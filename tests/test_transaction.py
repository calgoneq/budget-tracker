import pytest
from transaction import Transaction
from exceptions import ValidationError

def test_transaction_class_creates_object_with_correct_data():
    sklep: str = "biedronka"
    kwota: float = 12.03
    kategoria: str = "jedzenie"
    data: str = "2026-05-07"

    result = Transaction(sklep, kwota, kategoria, data)
    
    assert result.sklep == sklep
    assert result.kwota == kwota
    assert result.kategoria == kategoria
    assert result.data == data

def test_transaction_class_handles_price_validation_error():
    sklep: str = "biedronka"
    kategoria: str = "jedzenie"
    data: str = "2026-05-07"

    with pytest.raises(ValidationError):
        Transaction(sklep, -1.1, kategoria, data)
        
    with pytest.raises(ValidationError):
        Transaction(sklep, 0.0, kategoria, data)

def test_transaction_class_handles_data_validation_error():
    sklep: str = "biedronka"
    kwota: float = 12.3
    kategoria: str = "jedzenie"
    data: str = "2026+5-07"

    with pytest.raises(ValidationError):
        Transaction(sklep, kwota, kategoria, data)
    
def test_transaction_class_to_dict_method_returns_dict_with_correct_data():
    d: dict = {
        "sklep": "biedronka",
        "kwota": 12.4,
        "kategoria": "jedzenie",
        "data": "2026-05-04"
    }

    t = Transaction(sklep="biedronka", kwota=12.4, kategoria="jedzenie", data="2026-05-04")
    result = t.to_dict()

    assert result == d

def test_transaction_class_from_dict_method_returns_object_with_correct_attributes():
    d: dict = {
        "sklep": "biedronka",
        "kwota": 12.4,
        "kategoria": "jedzenie",
        "data": "2026-05-04"
    }

    result = Transaction.from_dict(d)

    assert result.sklep == d["sklep"]
    assert result.kwota == d["kwota"]
    assert result.kategoria == d["kategoria"]
    assert result.data == d["data"]

def test_transaction_class_from_dict_and_to_dict_response_equals_input():
    d: dict = {
        "sklep": "biedronka",
        "kwota": 12.4,
        "kategoria": "jedzenie",
        "data": "2026-05-04"
    }

    from_dict_result = Transaction.from_dict(d)

    result = from_dict_result.to_dict()

    assert result == d

def test_transaction_class_repr_has_sklep_and_kwota_fields():
    t = Transaction(sklep="biedronka", kwota=12.4, kategoria="jedzenie", data="2026-05-04")

    expected: str = "Transaction(sklep='biedronka', kwota=12.4, kategoria='jedzenie', data='2026-05-04')"

    assert repr(t) == expected

def test_transaction_dataclass_check_if_two_objects_equal():
    t1 = Transaction(sklep="biedronka", kwota=12.4, kategoria="jedzenie", data="2026-05-04")
    t2 = Transaction(sklep="biedronka", kwota=12.4, kategoria="jedzenie", data="2026-05-04")
    t3 = Transaction(sklep="lidl", kwota=12.4, kategoria="jedzenie", data="2026-05-04")

    assert t1 == t2

    assert t1 != t3