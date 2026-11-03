from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from src.infrastructure.db.db_connection import Base


class PayModel(Base):
    __tablename__ = "pays"

    pay_id = Column(String, primary_key=True)
    person_id = Column(String, ForeignKey("persons.person_id"), nullable=False)
    date = Column(String, nullable=False)
    url = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    is_advance = Column(Boolean, nullable=False)
