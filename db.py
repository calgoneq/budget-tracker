from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

from models_db import Base, TransactionModel

DATABASE_URL = "postgresql+asyncpg://calgoneq@localhost/budget_tracker"
engine = create_async_engine(DATABASE_URL)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_all_transactions(kategoria: str | None) -> list[dict]:
    async with AsyncSession(engine) as session:
        stmt = select(TransactionModel)
        if kategoria:
            stmt = stmt.where(TransactionModel.kategoria == kategoria)
        
        result = await session.execute(stmt)
        rows = result.scalars().all()
        response: list[dict] = [{"id": row.id, "sklep": row.sklep, "kwota": row.kwota, "kategoria": row.kategoria, "data": row.data, "notatka": row.notatka} for row in rows]

        return response
        
async def get_transaction_by_id(transaction_id: int) -> dict | None:
    async with AsyncSession(engine) as session:
        row = await session.get(TransactionModel, transaction_id)

        if row is None:
            return None
        
        response: dict = {"id": row.id, "sklep": row.sklep, "kwota": row.kwota, "kategoria": row.kategoria, "data": row.data, "notatka": row.notatka}
        return response

async def add_transaction(transaction: dict) -> dict:
    async with AsyncSession(engine) as session:
        new_t = TransactionModel(sklep=transaction["sklep"], kwota=transaction["kwota"], kategoria=transaction["kategoria"], data=transaction["data"], notatka=transaction.get("notatka"))
        session.add(new_t)
        await session.commit()
        await session.refresh(new_t)
        response: dict = {"id": new_t.id, "sklep": new_t.sklep, "kwota": new_t.kwota, "kategoria": new_t.kategoria, "data": new_t.data, "notatka": new_t.notatka}
        
        return response

async def remove_transaction(transaction_id: int) -> bool:
     async with AsyncSession(engine) as session:
        obj = await session.get(TransactionModel, transaction_id)
        if obj:
            await session.delete(obj)
            await session.commit()
            return True
        else:
            return False