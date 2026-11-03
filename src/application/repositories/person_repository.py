from src.domain.entities.person import Person
from abc import ABC, abstractmethod
from src.domain.value_objects.non_empty_string import NonEmptyString


class PersonRepository(ABC):
    @abstractmethod
    def save(self, person: Person) -> None:
        pass

    @abstractmethod
    def findById(self, id: NonEmptyString) -> Person | None:
        pass

    @abstractmethod
    def findByIds(self, ids: list[NonEmptyString]) -> list[Person] | None:
        pass

    @abstractmethod
    def findAll(self) -> list[Person] | None:
        pass

    @abstractmethod
    def delete(self, id: NonEmptyString) -> None:
        pass

    @abstractmethod
    def update(self, person: Person) -> None:
        pass
