from dataclasses import dataclass
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.non_empty_string import NonEmptyString


class InvalidPersonError(Exception):
    pass


@dataclass(eq=False)
class Person:
    person_id: NonEmptyString
    identification: NonEmptyString
    name: NonEmptyString
    email: NonEmptyString
    phone: Phone
    address: list[NonEmptyString]
    role: NonEmptyString

    def __post_init__(self):
        if (
            not isinstance(self.person_id, NonEmptyString)
            or not isinstance(self.identification, NonEmptyString)
            or not isinstance(self.name, NonEmptyString)
            or not isinstance(self.email, NonEmptyString)
            or not isinstance(self.phone, Phone)
            or not isinstance(self.address, list)
            or not isinstance(self.role, NonEmptyString)
        ):
            raise InvalidPersonError("The attributes of the Person instance is invalid")

        if "@" not in self.email:
            raise InvalidPersonError("The email attribute is invalid")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Person) and self.person_id == value.person_id
