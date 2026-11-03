from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path


ROOT_URL = Path(__file__).resolve().parents[3]
DB_PATH = str(ROOT_URL / "app.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    from src.infrastructure.db.tables.db_document_model import DocumentModel
    from src.infrastructure.db.tables.db_received_pay_model import ReceivedPayModel
    from src.infrastructure.db.tables.db_product_model import ProductModel
    from src.infrastructure.db.tables.db_person_model import PersonModel
    from src.infrastructure.db.tables.db_pay_model import PayModel
    from src.infrastructure.db.tables.db_emitted_pay_model import EmittedPayModel

    Base.metadata.create_all(bind=engine)
