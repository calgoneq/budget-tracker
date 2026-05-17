from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models_db import Base, TransactionModel

DATABASE_URL = "postgresql://calgoneq@localhost/budget_tracker"
engine = create_engine(DATABASE_URL)

def init_db() -> None:
    Base.metadata.create_all(engine)

def get_all_transactions(kategoria: str = None) -> list[dict]:
    with Session(engine) as session:
        if kategoria is not None:
            rows = session.query(TransactionModel).filter_by(kategoria=kategoria).all()
        else:
            rows = session.query(TransactionModel).all()

        list_of_dicts: list[dict] = [{"id": item.id, "sklep": item.sklep, "kwota": item.kwota, "kategoria": item.kategoria, "data": item.data, "notatka": item.notatka} for item in rows]
        return list_of_dicts
        
def get_transaction_by_id(transaction_id: int) -> dict | None:
    with Session(engine) as session:
        row = session.get(TransactionModel, transaction_id)

        if row is None:
            return None
        
        response: dict = {"id": row.id, "sklep": row.sklep, "kwota": row.kwota, "kategoria": row.kategoria, "data": row.data, "notatka": row.notatka}
        return response

def add_transaction(transaction: dict) -> dict:
    with Session(engine) as session:
        new_t = TransactionModel(sklep=transaction["sklep"], kwota=transaction["kwota"], kategoria=transaction["kategoria"], data=transaction["data"], notatka=transaction.get("notatka"))
        session.add(new_t)
        session.commit()
        session.refresh(new_t)
        response: dict = {"id": new_t.id, "sklep": new_t.sklep, "kwota": new_t.kwota, "kategoria": new_t.kategoria, "data": new_t.data, "notatka": new_t.notatka}
        
        return response

def remove_transaction(transaction_id: int) -> bool:
     with Session(engine) as session:
        obj = session.get(TransactionModel, transaction_id)
        if obj:
            session.delete(obj)
            session.commit()
            return True
        else:
            return False