from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.received_pay_repository import ReceivedPayRepository
from src.domain.value_objects.non_empty_string import NonEmptyString


class DeleteReceivedPayUseCase:
    def __init__(self, repository: ReceivedPayRepository):
        if not isinstance(repository, ReceivedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, id: NonEmptyString) -> None:
        self.repository.delete(id)
