from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from exceptions import ValidationError
from transaction import Transaction
from models import TransactionIn
from db import init_db, get_all_transactions, get_transaction_by_id, add_transaction, remove_transaction
from ai import generate_summary

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_status():
    return {"message": "server running"}

@app.get("/transactions")
async def get_transactions(kategoria: str = None):
    transactions = await get_all_transactions(kategoria)
    return transactions

@app.get("/transactions/summary")
async def get_summary():
    transaction = await get_all_transactions(None)
    try:
        ai_response = await generate_summary(transaction)
        return ai_response
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/transactions/{transaction_id}")
async def get_transactions_by_id(transaction_id: int):
    transaction = await get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail=f"Transakcja o id {transaction_id} nie istnieje")

    return transaction

@app.post("/transactions", status_code=201)
async def post_transaction(item: TransactionIn):
    try:
        transaction = Transaction(item.sklep, item.kwota, item.kategoria, item.data)
        data = transaction.to_dict()
        response = await add_transaction(data)
        return {"message": "ok", "transaction": response}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.delete("/transactions/{transaction_id}")
async def delete_transactions(transaction_id: int):
    if await remove_transaction(transaction_id):
        return {"message": f"Usunięto transakcje o id {transaction_id}"}
    else:
        raise HTTPException(status_code=404, detail=f"Transakcja o id {transaction_id} nie istnieje")