from src.domain.entities.person import Person
from src.application.errors.invalid_repository_error import InvalidRepositoryError
from src.application.repositories.person_repository import PersonRepository
from src.domain.value_objects.non_empty_string import NonEmptyString


class FindByIdPersonUseCase:
    def __init__(self, repository: PersonRepository):
        if not isinstance(repository, PersonRepository):
            raise InvalidRepositoryError(
                "Invalid Repository, cannot use it in a use case"
            )
        self.repository = repository

    def execute(self, id: NonEmptyString) -> Person | None:
        return self.repository.findById(id)
