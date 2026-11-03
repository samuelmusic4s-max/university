from sqlalchemy import Column, String, ForeignKey
from src.infrastructure.db.db_connection import Base


class EmittedPay(Base):
    __tablename__ = "emitted_pays"

    pay_id = Column(String, ForeignKey("pays.pay_id"), nullable=False)
    pay_emitted_id = Column(String, primary_key=True)
    recipient_account = Column(String, nullable=True)
