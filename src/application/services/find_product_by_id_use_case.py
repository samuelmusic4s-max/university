from src.domain.entities.product import Product
from src.application.repositories.product_repository import ProductRepository
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.domain.value_objects.non_empty_string import NonEmptyString


class FindProductByIdUseCase:
    def __init__(self, repository: ProductRepository):
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError("Cannot use an invalid repository")
        self.repository = repository

    def execute(self, id: NonEmptyString) -> Product | None:
        return self.repository.findById(id)
