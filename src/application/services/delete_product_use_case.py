from src.application.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.domain.value_objects.non_empty_string import NonEmptyString


class DeleteProductUseCase:
    def __init__(self, repository: ProductRepository):
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError(
                "Invalid product repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, id: NonEmptyString):
        self.repository.delete(id)
