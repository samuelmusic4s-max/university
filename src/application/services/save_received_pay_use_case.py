from src.domain.entities.received_pay import ReceivedPay
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.errors.item_already_exists_error import ItemAlreadyExistsError
from src.application.repositories.received_pay_repository import ReceivedPayRepository


class SaveReceivedPayUseCase:
    def __init__(self, repository: ReceivedPayRepository):
        if not isinstance(repository, ReceivedPayRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, data: ReceivedPay) -> None:
        if self.repository.findById(data.received_pay_id) is not None:
            raise ItemAlreadyExistsError("Cannot save a ReceivedPay that already exists")
        self.repository.save(data)
