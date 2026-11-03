from src.infrastructure.db.tables.db_product_model import ProductModel
from src.application.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.infrastructure.db.db_connection import SessionLocal
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.application.errors.item_does_not_exists_error import ItemDoesNotExistsError


class SqliteProductRepository(ProductRepository):
    def save(self, data: Product):
        db_product = ProductModel(
            product_id=str(data.product_id),
            name=str(data.name),
            price=float(data.price),
            description=str(data.description),
            categories=[str(c) for c in data.categories],
            img_url=str(data.img_url),
            state=str(data.state),
        )

        with SessionLocal() as session:
            try:
                session.add(db_product)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def _to_entity(self, model: ProductModel) -> Product:
        return Product(
            product_id=NonEmptyString(model.product_id),
            name=NonEmptyString(model.name),
            categories=[NonEmptyString(x) for x in model.categories],
            price=float(model.price),
            description=NonEmptyString(model.description),
            state=NonEmptyString(model.state),
            img_url=NonEmptyString(model.img_url),
        )

    def findById(self, id: NonEmptyString) -> Product | None:
        with SessionLocal() as session:
            db_product = session.get(ProductModel, str(id))
            if db_product is None:
                return None
            return self._to_entity(db_product)

    def findByIds(self, ids: list[NonEmptyString]) -> list[Product | None]:
        id_strings = [str(item) for item in ids]
        with SessionLocal() as session:
            db_products = (
                session.query(ProductModel)
                .filter(ProductModel.product_id.in_(id_strings))
                .all()
            )
            return [self._to_entity(p) for p in db_products]

    def update(self, data: Product) -> None:
        with SessionLocal() as session:
            try:
                db_data = session.get(ProductModel, str(data.product_id))
                if db_data is None:
                    raise ItemDoesNotExistsError(
                        "Cannot update a product that doesn't exists"
                    )

                db_data.state = str(data.state)
                db_data.img_url = str(data.img_url)
                db_data.description = str(data.description)
                db_data.price = float(data.price)
                db_data.categories = [str(x) for x in data.categories]
                db_data.name = str(data.name)

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def findAll(self) -> list[Product] | None:
        with SessionLocal() as session:
            db_products = session.query(ProductModel).all()
            return [self._to_entity(p) for p in db_products]

    def delete(self, id: NonEmptyString) -> None:
        with SessionLocal() as session:
            try:
                db_data = session.get(ProductModel, str(id))
                if db_data is None:
                    raise ItemDoesNotExistsError(
                        "Cannot delete a product that doesn't exists"
                    )
                session.delete(db_data)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
