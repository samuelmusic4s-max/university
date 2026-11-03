from dataclasses import dataclass
from src.domain.value_objects.non_empty_string import NonEmptyString


class InvalidPayError(Exception):
    pass


@dataclass(eq=False)
class Pay:
    person_id: NonEmptyString
    pay_id: NonEmptyString
    date: NonEmptyString
    url: NonEmptyString
    amount: float
    method: NonEmptyString
    reason: NonEmptyString
    is_advance: bool

    def __post_init__(self):
        if (
            not isinstance(self.pay_id, NonEmptyString)
            or not isinstance(self.date, NonEmptyString)
            or not isinstance(self.url, NonEmptyString)
            or not isinstance(self.person_id, NonEmptyString)
            or not isinstance(self.amount, float)
            or not isinstance(self.method, NonEmptyString)
            or not isinstance(self.reason, NonEmptyString)
            or not isinstance(self.is_advance, bool)
        ):
            raise InvalidPayError("The attributes are invalid of Pay are invalid")
        if self.amount <= 0:
            raise InvalidPayError("The amount of the pay cannot be zero or negative")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Pay) and self.pay_id == value.pay_id
