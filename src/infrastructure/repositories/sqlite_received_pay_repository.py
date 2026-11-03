from src.application.repositories.received_pay_repository import ReceivedPayRepository
from src.domain.entities.received_pay import ReceivedPay
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.infrastructure.db.tables.db_received_pay_model import ReceivedPayModel
from src.infrastructure.db.db_connection import SessionLocal
from src.infrastructure.db.tables.db_pay_model import PayModel
from src.application.errors.item_does_not_exists_error import ItemDoesNotExistsError


class SqliteReceivedPay(ReceivedPayRepository):
    def save(self, pay: ReceivedPay) -> None:
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
        db_received = ReceivedPayModel(
            pay_id=str(pay.pay_id),
            received_pay_id=str(pay.received_pay_id),
            net_amount=float(pay.net_amount) if pay.net_amount is not None else float(pay.amount),
            interest=float(pay.interest),
        )

        with SessionLocal() as session:
            try:
                session.add(db_pay)
                session.add(db_received)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def _to_entity(
        self, pay_model: PayModel, received_model: ReceivedPayModel
    ) -> ReceivedPay:
        return ReceivedPay(
            person_id=NonEmptyString(pay_model.person_id),
            pay_id=NonEmptyString(pay_model.pay_id),
            date=NonEmptyString(pay_model.date),
            url=NonEmptyString(pay_model.url),
            amount=float(pay_model.amount),
            method=NonEmptyString(pay_model.method),
            reason=NonEmptyString(pay_model.reason),
            is_advance=bool(pay_model.is_advance),
            received_pay_id=NonEmptyString(received_model.received_pay_id),
            net_amount=float(received_model.net_amount),
            interest=float(received_model.interest),
        )

    def findById(self, id: NonEmptyString) -> ReceivedPay | None:
        with SessionLocal() as session:
            db_received = session.get(ReceivedPayModel, str(id))
            if db_received is None:
                return None
            db_pay = session.get(PayModel, str(db_received.pay_id))
            if db_pay is None:
                return None
            return self._to_entity(db_pay, db_received)

    def findAll(self) -> list[ReceivedPay] | None:
        with SessionLocal() as session:
            rows = (
                session.query(PayModel, ReceivedPayModel)
                .join(ReceivedPayModel, PayModel.pay_id == ReceivedPayModel.pay_id)
                .all()
            )
            return [self._to_entity(pay, received) for pay, received in rows]

    def findByIds(self, ids: list[NonEmptyString]) -> list[ReceivedPay] | None:
        list_ids = [str(id) for id in ids]
        with SessionLocal() as session:
            rows = (
                session.query(PayModel, ReceivedPayModel)
                .join(ReceivedPayModel, PayModel.pay_id == ReceivedPayModel.pay_id)
                .filter(ReceivedPayModel.received_pay_id.in_(list_ids))
                .all()
            )
            return [self._to_entity(pay, received) for pay, received in rows]

    def update(self, pay: ReceivedPay) -> None:
        with SessionLocal() as session:
            try:
                db_received = session.get(ReceivedPayModel, str(pay.received_pay_id))
                if db_received is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update a pay that doesn't exist"
                    )
                db_pay = session.get(PayModel, str(pay.pay_id))
                if db_pay is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update a pay that doesn't exist"
                    )
                db_pay.person_id = str(pay.person_id)
                db_pay.date = str(pay.date)
                db_pay.url = str(pay.url)
                db_pay.amount = float(pay.amount)
                db_pay.method = str(pay.method)
                db_pay.reason = str(pay.reason)
                db_pay.is_advance = bool(pay.is_advance)

                db_received.net_amount = (
                    float(pay.net_amount)
                    if pay.net_amount is not None
                    else float(pay.amount)
                )
                db_received.interest = float(pay.interest)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: NonEmptyString) -> None:
        with SessionLocal() as session:
            try:
                db_received = session.get(ReceivedPayModel, str(id))
                if db_received is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete a pay that doesn't exist"
                    )
                db_pay = session.get(PayModel, str(db_received.pay_id))
                if db_pay is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete a pay that doesn't exist"
                    )

                session.delete(db_received)
                session.delete(db_pay)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
