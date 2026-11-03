from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.emitted_pay_repository import EmittedPayRepository
from src.domain.value_objects.non_empty_string import NonEmptyString


class DeleteEmittedPayUseCase:
    def __init__(self, repository: EmittedPayRepository):
        if not isinstance(repository, EmittedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, id: NonEmptyString) -> None:
        self.repository.delete(id)
