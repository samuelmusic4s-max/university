from sqlalchemy import Column, String, Float, ForeignKey
from src.infrastructure.db.db_connection import Base


class ReceivedPayModel(Base):
    __tablename__ = "received_pays"

    pay_id = Column(String, ForeignKey("pays.pay_id"), nullable=False)
    received_pay_id = Column(String, primary_key=True)
    net_amount = Column(Float, nullable=False)
    interest = Column(Float, nullable=False)
