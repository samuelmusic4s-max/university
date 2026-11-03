from dataclasses import dataclass
from src.domain.value_objects.non_empty_string import NonEmptyString


class InvalidProductError(Exception):
    pass


@dataclass(eq=False)
class Product:
    product_id: NonEmptyString
    categories: list[NonEmptyString]
    price: float
    description: NonEmptyString
    name: NonEmptyString
    state: NonEmptyString
    img_url: NonEmptyString

    def __post_init__(self):
        if (
            not isinstance(self.product_id, NonEmptyString)
            or not isinstance(self.categories, list)
            or not isinstance(self.description, NonEmptyString)
            or not isinstance(self.name, NonEmptyString)
            or not isinstance(self.price, float)
            or not isinstance(self.state, NonEmptyString)
            or not isinstance(self.img_url, NonEmptyString)
        ):
            raise InvalidProductError(
                "Cannot create a product with data that is not valid"
            )

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Product) and self.product_id == value.product_id
