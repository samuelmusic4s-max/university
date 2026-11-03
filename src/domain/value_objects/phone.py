from dataclasses import dataclass
from src.domain.value_objects.non_empty_string import NonEmptyString


class InvalidPhoneError(Exception):
    pass


@dataclass
class Phone:
    value: NonEmptyString
    postal_code: NonEmptyString

    def __post_init__(self):
        if not isinstance(self.value, NonEmptyString) or not isinstance(self.postal_code, NonEmptyString):
            raise InvalidPhoneError("Cannot create an invalid phone number")
        if not self.value.isnumeric() or len(self.value) != 10:
            raise InvalidPhoneError("The number phone must be an string of 10 numbers")
        if not self.postal_code.isnumeric() or len(self.postal_code) > 3:
            raise InvalidPhoneError(
                "The postal code is a number less than one thousand"
            )
