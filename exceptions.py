class BudgetError(Exception):
    """Bazowy wyjątek dla całego projektu."""
    pass

class StorageError(BudgetError):
    """Błędy warstwy storage."""
    pass

class FileCorruptedError(StorageError):
    """Plik JSON istnieje ale jest uszkodzony."""
    pass

class FileWriteError(StorageError):
    """Nie udało się zapisać danych do pliku JSON."""
    pass

class ValidationError(BudgetError):
    """Błąd walidacji danych."""
    pass