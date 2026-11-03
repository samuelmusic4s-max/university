from src.application.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.application.errors.invalid_repository_error import InvalidRepositoryError


class FindProductsByIdsUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError(
                "Invalid repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, ids: list[NonEmptyString]) -> list[Product | None]:
        return self.repository.findByIds(ids)
