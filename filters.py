from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

def parse_date(data: str) -> date:
    '''Converts string into a datetime.date object.'''
    try:
        d = datetime.strptime(data, "%Y-%m-%d").date()
        return d

    except ValueError:
        if len(data) == 0:
            logger.warning(f"ERROR: data nie powinna być pusta")
        else: 
            logger.error(f"ERROR: {data} nie pasuje do formatu, spróbuj YYYY-MM-DD")

        raise

def sort_transaction_by_date(transactions: list[dict]) -> list[dict]:
    '''Sorts list of items by data and returns it'''
    sorted_transactions = sorted(transactions, key=lambda t: (1, "") if not t.get("data") else (0, t["data"]))

    return sorted_transactions

def filter_by_date_range(transactions: list[dict], od: str = None , do: str = None) -> list[dict]:
    '''filers transactions based on range from - to'''
    date_od: datetime.date = parse_date(od) if od is not None else None
    date_do: datetime.date = parse_date(do) if do is not None else None
    
    result: list = []

    for t in transactions:

        try:
            d = parse_date(t.get("data", ""))
        except ValueError:
            continue

        if date_od is not None and d < date_od:
            continue
        if date_do is not None and d > date_do:
            continue

        result.append(t)
            
    return result