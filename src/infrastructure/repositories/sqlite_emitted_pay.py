from src.application.repositories.emitted_pay_repository import EmittedPayRepository
from src.domain.entities.emitted_pay import EmittedPay
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.infrastructure.db.tables.db_emitted_pay_model import EmittedPayModel
from src.infrastructure.db.db_connection import SessionLocal
from src.domain.entities.pay import Pay
from src.infrastructure.db.tables.db_pay_model import PayModel
from src.application.errors.item_does_not_exists_error import ItemDoesNotExistsError
from src.application.errors.item_already_exists_error import ItemAlreadyExistsError


class SqliteEmittedPay(EmittedPayRepository):
    def save(self, pay: EmittedPay) -> None:
        db_pay = PayModel(
            pay_id=str(pay.pay_id),
            person_id=str(pay.person_id),
            date=str(pay.date),
            url=str(pay.url),
            amount=float(pay.amount),
            method=str(pay.method),
            reason=str(pay.reason),
            is_advance=bool(pay.is_advance),
        )
        db_emitted = EmittedPayModel(
            pay_id=str(pay.pay_id),
            pay_emitted_id=str(pay.pay_emitted_id),
            recipient_account=str(pay.recipient_account),
        )

        with SessionLocal() as session:
            try:
                session.add(db_pay)
                session.add(db_emitted)
                session.commit()

            except Exception as e:
                session.rollback()
                raise e

    def _to_entity(
        self, pay_model: PayModel, emitted_model: EmittedPayModel
    ) -> EmittedPay:
        return EmittedPay(
            person_id=NonEmptyString(pay_model.person_id),
            pay_id=NonEmptyString(pay_model.pay_id),
            date=NonEmptyString(pay_model.date),
            url=NonEmptyString(pay_model.url),
            amount=float(pay_model.amount),
            method=NonEmptyString(pay_model.method),
            reason=NonEmptyString(pay_model.reason),
            is_advance=bool(pay_model.is_advance),
            pay_emitted_id=NonEmptyString(emitted_model.pay_emitted_id),
            recipient_account=NonEmptyString(emitted_model.recipient_account),
        )

    def findById(self, id: NonEmptyString) -> EmittedPay | None:
        with SessionLocal() as session:
            db_emitted = session.get(EmittedPayModel, str(id))
            if db_emitted is None:
                return None
            db_pay = session.get(PayModel, str(db_emitted.pay_id))
            if db_pay is None:
                return None
            return self._to_entity(db_pay, db_emitted)

    def findAll(self) -> list[EmittedPay] | None:
        with SessionLocal() as session:
            rows = (
                session.query(PayModel, EmittedPayModel)
                .join(EmittedPayModel, PayModel.pay_id == EmittedPayModel.pay_id)
                .all()
            )
            return [self._to_entity(pay, emitted) for pay, emitted in rows]

    def findByIds(self, ids: list[NonEmptyString]) -> list[EmittedPay] | None:
        list_ids = [str(id) for id in ids]
        with SessionLocal() as session:
            rows = (
                session.query(PayModel, EmittedPayModel)
                .join(EmittedPayModel, PayModel.pay_id == EmittedPayModel.pay_id)
                .filter(EmittedPayModel.pay_emitted_id.in_(list_ids))
                .all()
            )
            return [self._to_entity(pay, emitted) for pay, emitted in rows]

    def update(self, pay: EmittedPay) -> None:
        with SessionLocal() as session:
            try:
                db_emitted = session.get(EmittedPayModel, str(pay.pay_emitted_id))
                if db_emitted is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update an pay that doesn't exists"
                    )
                db_pay = session.get(PayModel, str(pay.pay_id))

                if db_pay is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update an pay that doesn't exists"
                    )
                db_pay.person_id = str(pay.person_id)
                db_pay.date = str(pay.date)
                db_pay.url = str(pay.url)
                db_pay.amount = float(pay.amount)
                db_pay.method = str(pay.method)
                db_pay.reason = str(pay.reason)
                db_pay.is_advance = bool(pay.is_advance)

                db_emitted.recipient_account = str(pay.recipient_account)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: NonEmptyString) -> None:
        with SessionLocal() as session:
            try:
                db_emitted = session.get(EmittedPayModel, str(id))
                if db_emitted is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete an pay that doesn't exists"
                    )
                db_pay = session.get(PayModel, str(db_emitted.pay_id))
                if db_pay is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete an pay that doesn't exists"
                    )

                session.delete(db_emitted)
                session.delete(db_pay)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
