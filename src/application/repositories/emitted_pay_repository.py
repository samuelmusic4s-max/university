from abc import ABC, abstractmethod
from src.domain.entities.emitted_pay import EmittedPay
from src.domain.value_objects.non_empty_string import NonEmptyString


class EmittedPayRepository(ABC):
    @abstractmethod
    def save(self, pay: EmittedPay) -> None:
        pass

    @abstractmethod
    def findById(self, id: NonEmptyString) -> EmittedPay | None:
        pass

    @abstractmethod
    def findByIds(self, ids: list[NonEmptyString]) -> list[EmittedPay] | None:
        pass

    @abstractmethod
    def update(self, pay: EmittedPay) -> None:
        pass

    @abstractmethod
    def delete(self, id: NonEmptyString) -> None:
        pass

    @abstractmethod
    def findAll(self) -> list[EmittedPay] | None:
        pass
