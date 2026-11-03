from sqlalchemy import Column, String, Integer, Date
from src.infrastructure.db.db_connection import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
