from sqlalchemy import Column, String, Float, Integer, JSON
from src.infrastructure.db.db_connection import Base


class ProductModel(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    categories = Column(JSON, default=list)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    state = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
