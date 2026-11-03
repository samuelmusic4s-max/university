from src.domain.exceptions.empty_string_error import EmptyStringError
from src.domain.exceptions.invalid_string_error import InvalidStringError


class NonEmptyString(str):
    """
    Value Object representing a validated, non-empty string.
    
    Invariants:
    - Must be of type `str`.
    - Cannot be empty or contain only whitespace characters.
    
    Inheriting from `str` guarantees:
    - Immutability out-of-the-box.
    - Seamless interoperability with standard string operations, PySide6, and serialization.
    - Preserves `isinstance(val, str)` compatibility while enabling `isinstance(val, NonEmptyString)`.
    """

    def __new__(cls, value: object):
        if not isinstance(value, str):
            raise InvalidStringError(
                f"Expected str, got {type(value).__name__}: {value!r}"
            )

        if not value.strip():
            raise EmptyStringError("String cannot be empty or whitespace-only")

        return super().__new__(cls, value)


# Alias to support both naming styles
NoEmptyString = NonEmptyString
