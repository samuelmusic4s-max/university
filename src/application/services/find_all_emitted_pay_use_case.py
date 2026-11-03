from src.domain.entities.emitted_pay import EmittedPay
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.emitted_pay_repository import EmittedPayRepository


class FindAllEmittedPayUseCase:
    def __init__(self, repository: EmittedPayRepository):
        if not isinstance(repository, EmittedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self) -> list[EmittedPay] | None:
        return self.repository.findAll()
