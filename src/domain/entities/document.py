from dataclasses import dataclass
from src.domain.value_objects.non_empty_string import NonEmptyString


class InvalidDocumentError(Exception):
    pass


@dataclass(eq=False)
class Document:
    document_id: NonEmptyString
    date: NonEmptyString
    quantity: float

    def __post_init__(self):
        if (
            not isinstance(self.document_id, NonEmptyString)
            or not isinstance(self.date, NonEmptyString)
            or not isinstance(self.quantity, float)
        ):
            raise InvalidDocumentError("The attributes are invalid")
        if self.quantity <= 0:
            raise InvalidDocumentError("The price cannot be negative or zero")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Document) and self.document_id == value.document_id
