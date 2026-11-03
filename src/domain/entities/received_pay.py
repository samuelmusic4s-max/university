from dataclasses import dataclass
from src.domain.entities.pay import Pay, InvalidPayError
from src.domain.value_objects.non_empty_string import NonEmptyString


@dataclass(eq=False)
class ReceivedPay(Pay):
    received_pay_id: NonEmptyString
    net_amount: float | None
    interest: float

    def __post_init__(self):
        super().__post_init__()
        if (
            not isinstance(self.received_pay_id, NonEmptyString)
            or not isinstance(self.interest, float)
            or (self.net_amount is not None and not isinstance(self.net_amount, float))
        ):
            raise InvalidPayError("Cannot create a ReceivedPay with wrong attributes")
        if self.interest < 0:
            raise InvalidPayError("The interest cannot be less than zero")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ReceivedPay)
            and self.received_pay_id == value.received_pay_id
        )
