from src.domain.entities.received_pay import ReceivedPay
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.received_pay_repository import ReceivedPayRepository


class UpdateReceivedPayUseCase:
    def __init__(self, repository: ReceivedPayRepository):
        if not isinstance(repository, ReceivedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, pay: ReceivedPay) -> None:
        self.repository.update(pay)
