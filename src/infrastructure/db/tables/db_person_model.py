from sqlalchemy import Column, String, JSON
from src.infrastructure.db.db_connection import Base


class PersonModel(Base):
    __tablename__ = "persons"

    person_id = Column(String, primary_key=True)
    identification = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(JSON, nullable=False)
    address = Column(JSON, default=list)
    role = Column(String, nullable=False)
