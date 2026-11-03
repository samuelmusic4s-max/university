from src.application.repositories.product_repository import ProductRepository
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.domain.entities.product import Product


class UpdateProductUseCase:
    def __init__(self, repository: ProductRepository):
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError(
                "Invalid repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, data: Product) -> None:
        self.repository.update(data)
