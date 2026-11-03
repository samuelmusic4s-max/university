from abc import ABC, abstractmethod
from src.domain.entities.received_pay import ReceivedPay
from src.domain.value_objects.non_empty_string import NonEmptyString


class ReceivedPayRepository(ABC):
    @abstractmethod
    def save(self, pay: ReceivedPay) -> None:
        pass

    @abstractmethod
    def findById(self, id: NonEmptyString) -> ReceivedPay | None:
        pass

    @abstractmethod
    def findByIds(self, ids: list[NonEmptyString]) -> list[ReceivedPay] | None:
        pass

    @abstractmethod
    def update(self, pay: ReceivedPay) -> None:
        pass

    @abstractmethod
    def delete(self, id: NonEmptyString) -> None:
        pass

    @abstractmethod
    def findAll(self) -> list[ReceivedPay] | None:
        pass
