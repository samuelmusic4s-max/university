from src.application.repositories.person_repository import PersonRepository
from src.domain.entities.person import Person
from src.infrastructure.db.tables.db_person_model import PersonModel
from src.infrastructure.db.db_connection import SessionLocal
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.domain.value_objects.phone import Phone
from src.application.errors.item_does_not_exists_error import ItemDoesNotExistsError


class SqlitePersonRepository(PersonRepository):
    def save(self, person: Person) -> None:
        db_person = PersonModel(
            person_id=str(person.person_id),
            identification=str(person.identification),
            name=str(person.name),
            email=str(person.email),
            phone={
                "value": str(person.phone.value),
                "postal_code": str(person.phone.postal_code),
            },
            address=[str(d) for d in person.address],
            role=str(person.role),
        )

        with SessionLocal() as session:
            try:
                session.add(db_person)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def _to_entity(self, data: PersonModel) -> Person:
        return Person(
            NonEmptyString(data.person_id),
            NonEmptyString(data.identification),
            NonEmptyString(data.name),
            NonEmptyString(data.email),
            Phone(
                NonEmptyString(data.phone["value"]),
                NonEmptyString(data.phone["postal_code"]),
            ),
            [NonEmptyString(a) for a in data.address],
            NonEmptyString(data.role),
        )

    def findById(self, id: NonEmptyString) -> Person | None:
        with SessionLocal() as session:
            db_product = session.get(PersonModel, str(id))
            if db_product is None:
                return None
            return self._to_entity(db_product)

    def findByIds(self, ids: list[NonEmptyString]) -> list[Person] | None:
        list_ids = [str(id) for id in ids]
        with SessionLocal() as session:
            persons = (
                session.query(PersonModel)
                .filter(PersonModel.person_id.in_(list_ids))
                .all()
            )
            return [self._to_entity(person) for person in persons]

    def findAll(self) -> list[Person] | None:
        with SessionLocal() as session:
            persons = session.query(PersonModel).all()
            return [self._to_entity(person) for person in persons]

    def update(self, person: Person) -> None:
        with SessionLocal() as session:
            try:
                db_person = session.get(PersonModel, str(person.person_id))
                if db_person is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update an Person that does not exists"
                    )

                db_person.identification = str(person.identification)
                db_person.name = str(person.name)
                db_person.email = str(person.email)
                db_person.phone = {
                    "value": str(person.phone.value),
                    "postal_code": str(person.phone.postal_code),
                }
                db_person.address = [str(a) for a in person.address]
                db_person.role = str(person.role)

                session.commit()

            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: NonEmptyString) -> None:
        with SessionLocal() as session:
            try:
                db_person = session.get(PersonModel, str(id))
                if db_person is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete an item that does not exists"
                    )

                session.delete(db_person)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e
