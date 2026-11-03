from dataclasses import dataclass
from src.domain.entities.pay import Pay, InvalidPayError
from src.domain.value_objects.non_empty_string import NonEmptyString


@dataclass(eq=False)
class EmittedPay(Pay):
    pay_emitted_id: NonEmptyString
    recipient_account: NonEmptyString

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.pay_emitted_id, NonEmptyString) or not isinstance(
            self.recipient_account, NonEmptyString
        ):
            raise InvalidPayError("Cannot create an pay emitted with wrong attributes")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, EmittedPay)
            and self.pay_emitted_id == value.pay_emitted_id
        )
