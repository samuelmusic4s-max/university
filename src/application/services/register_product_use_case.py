from src.domain.entities.product import Product
from src.application.repositories.product_repository import ProductRepository
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.errors.item_already_exists_error import (
    ItemAlreadyExistsError,
)


class RegisterProductUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        if not isinstance(repository, ProductRepository):
            raise InvalidRepositoryError(
                "If the repository is invalid, can't use the use_case"
            )
        self.repository = repository

    def execute(self, data: Product) -> None:
        if self.repository.findById(data.product_id) is not None:
            raise ItemAlreadyExistsError("Cannot save a Item that already exists")
        self.repository.save(data)
