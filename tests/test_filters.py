import pytest
from datetime import date as d

from filters import parse_date, filter_by_date_range, sort_transaction_by_date

def test_parse_date_returns_datetime_date_object():
    date: str = "2026-05-04"

    result = parse_date(date)
    assert result == d(2026, 5, 4)

def test_parse_date_raises_value_error_for_wrong_data():
    date: str = "abc"

    with pytest.raises(ValueError):
        parse_date(date)

def test_parse_date_raises_value_error_for_empty_data():
    date: str = ""

    with pytest.raises(ValueError):
        parse_date(date)

def test_sort_transaction_by_date_correctly_sorts__unordered_list():
    data: list[dict] = [
        {"data": "2026-05-04", "kwota": 50},
        {"data": "2026-05-18", "kwota": 50},
        {"data": "2026-06-24", "kwota": 50},
        {"data": "2026-04-15", "kwota": 30}
    ]

    sorted_data: list[dict] = [
        {"data": "2026-04-15", "kwota": 30},
        {"data": "2026-05-04", "kwota": 50},
        {"data": "2026-05-18", "kwota": 50},
        {"data": "2026-06-24", "kwota": 50},
    ]

    result = sort_transaction_by_date(data)

    assert sorted_data == result

def test_sort_transaction_by_date_returns_empty_list_if_empty():
    data: list = []

    result = sort_transaction_by_date(data)

    assert data == result

def test_filter_by_date_range_returns_only_april_transactions():
    data: list[dict] = [
        {"data": "2026-04-04", "kwota": 50},
        {"data": "2026-05-18", "kwota": 50},
        {"data": "2026-06-24", "kwota": 50},
        {"data": "2026-04-15", "kwota": 30}
    ]

    result = filter_by_date_range(data, "2026-04-01", "2026-04-30")

    assert result == [{"data": "2026-04-04", "kwota": 50}, {"data": "2026-04-15", "kwota": 30}]

def test_filter_by_date_range_none_end_of_april_returns_all_transactions_until_end_of_april():
    data: list[dict] = [
        {"data": "2026-04-04", "kwota": 50},
        {"data": "2026-05-18", "kwota": 50},
        {"data": "2026-03-24", "kwota": 50},
        {"data": "2026-04-15", "kwota": 30}
    ]

    result = filter_by_date_range(data, None, "2026-04-30")

    assert result == [{"data": "2026-04-04", "kwota": 50}, {"data": "2026-03-24", "kwota": 50}, {"data": "2026-04-15", "kwota": 30}]

def test_filter_by_date_range_none_to_none_returns_all_transactions():
    data: list[dict] = [
        {"data": "2026-04-04", "kwota": 50},
        {"data": "2026-05-18", "kwota": 50},
        {"data": "2026-03-24", "kwota": 50},
        {"data": "2026-04-15", "kwota": 30}
    ]

    result = filter_by_date_range(data, None, None)

    assert result == data

