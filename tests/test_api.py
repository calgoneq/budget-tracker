import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from main import app
import db

client = TestClient(app)
TEST_DATABASE_URL = "postgresql://calgoneq@localhost/budget_test"
test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    monkeypatch.setattr(db, "engine", test_engine)
    db.init_db()
    with Session(test_engine) as session:
        session.execute(text("DELETE FROM transactions"))
        session.commit()
    
def test_get_transaction():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.parametrize("sklep, kwota, kategoria, data, expected_status", [
    ("test_sklep", 10.2, "test_category", "2026-02-12", 201),
    ("test_sklep_incorrect_kwota", -10.2, "test_category_incorrect_kwota", "2026-02-12", 422),
    ("test_sklep_incorrect_kwota", 10.2, "test_category_incorrect_kwota", "abc", 422)
])

def test_post_transaction(sklep, kwota, kategoria, data, expected_status):
    body: dict = {
        "sklep": sklep,
        "kwota": kwota,
        "kategoria": kategoria,
        "data": data,
    }
    
    response = client.post("/transactions", json=body)
    assert response.status_code == expected_status

def test_get_after_new_transaction_returns_correct_json():
    new_transaction: dict = {
        "sklep": "test_sklep",
        "kwota": 10.2,
        "kategoria": "test_category",
        "data": "2026-02-12",
    }
    client.post("/transactions", json=new_transaction)

    response = client.get("/transactions")
    data = response.json()

    assert response.status_code == 200
    assert any(t["sklep"] == "test_sklep" for t in data)

def test_get_with_kategoria_parameter_returns_correct_data():
    new_transactions: dict = {
        "sklep": "test_sklep",
        "kwota": 10.2,
        "kategoria": "jedzenie",
        "data": "2026-02-12",
    }
    client.post("/transactions", json=new_transactions)

    response = client.get("/transactions?kategoria=jedzenie")
    data = response.json()
    assert response.status_code == 200
    assert any(t["kategoria"] == "jedzenie" for t in data)

def test_get_transaction_with_id_returns_only_transaction_with_correct_id():
    transaction_1: dict = {
        "sklep": "domino",
        "kwota": 18.5,
        "kategoria": "psy",
        "data": "2026-02-18",
    }

    post_response = client.post("/transactions", json=transaction_1)
    created_data = post_response.json()

    assigned_id = created_data["transaction"]["id"]
    response = client.get(f"/transactions/{assigned_id}")
    data = response.json()

    assert response.status_code == 200
    assert assigned_id == data["id"]
    assert transaction_1["kategoria"] == data["kategoria"]

def test_get_transaction_with_incorrect_id_returns_404():
    transaction_id: int = 200
    response = client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 404
    data = response.json()
    assert str(transaction_id) in data["detail"]

def test_delete_transaction_removes_and_returns_200():
    transaction_1: dict = {
        "sklep": "domino",
        "kwota": 18.5,
        "kategoria": "psy",
        "data": "2026-02-18",
    }

    post_response = client.post("/transactions", json=transaction_1)
    created_data = post_response.json()
    assigned_id = created_data["transaction"]["id"]

    before_delete = client.get('/transactions')
    before_data = before_delete.json()

    response = client.delete(f"/transactions/{assigned_id}")
    assert response.status_code == 200

    after_delete = client.get('/transactions')
    after_data = after_delete.json()

    assert len(before_data) > len(after_data)