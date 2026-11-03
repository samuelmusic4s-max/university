from abc import ABC, abstractmethod
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def findById(self, id: NonEmptyString) -> Product | None:
        pass

    @abstractmethod
    def findByIds(self, ids: list[NonEmptyString]) -> list[Product | None]:
        pass

    @abstractmethod
    def save(self, data: Product) -> None:
        pass

    @abstractmethod
    def update(self, data: Product) -> None:
        pass

    @abstractmethod
    def findAll(self) -> list[Product] | None:
        pass

    @abstractmethod
    def delete(self, id: NonEmptyString) -> None:
        pass
