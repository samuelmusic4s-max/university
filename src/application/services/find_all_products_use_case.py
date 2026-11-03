from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product


class FindAllProductsUseCase:
    def __init__(self, repository: ProductRepository):
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError(
                "Invalid repository, cannot be used in a use case"
            )
        self.repository = repository

    def execute(self) -> list[Product] | None:
        return self.repository.findAll()
