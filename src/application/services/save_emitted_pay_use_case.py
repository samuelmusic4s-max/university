from src.domain.entities.emitted_pay import EmittedPay
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.errors.item_already_exists_error import ItemAlreadyExistsError
from src.application.repositories.emitted_pay_repository import EmittedPayRepository


class SaveEmittedPayUseCase:
    def __init__(self, repository: EmittedPayRepository):
        if not isinstance(repository, EmittedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, data: EmittedPay) -> None:
        if self.repository.findById(data.pay_emitted_id) is not None:
            raise ItemAlreadyExistsError("Cannot save an EmittedPay that already exists")
        self.repository.save(data)
