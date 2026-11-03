from src.domain.entities.person import Person
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.person_repository import PersonRepository
from src.application.errors.item_already_exists_error import ItemAlreadyExistsError


class SavePersonUseCase:
    def __init__(self, repository: PersonRepository):
        if not isinstance(repository, PersonRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, data: Person) -> None:
        if self.repository.findById(data.person_id) is not None:
            raise ItemAlreadyExistsError(
                "An person that already is the database cannot be saved again"
            )
        self.repository.save(data)
