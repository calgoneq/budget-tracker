from dataclasses import dataclass, asdict

from exceptions import ValidationError
from filters import parse_date

@dataclass()
class Transaction:
    """Szkielet każdej tranzakcji + walidacja kwoty i daty"""
    sklep: str
    kwota: float
    kategoria: str
    data: str

    def __post_init__(self):
        if self.kwota <= 0:
            raise ValidationError(f"kwota musi być większa od 0, otrzymano {self.kwota}")

        try:
            d = parse_date(self.data)
            self.data = d.isoformat()
        except ValueError as e:
            message = f"data {self.data} format is incorrect, try YYYY-MM-DD"
            raise ValidationError(message) from e

    # def __init__(self, sklep: str, kwota: float, kategoria: str, data: str):
    #     if kwota <= 0:
    #         raise ValidationError(f"kwota musi być większa od 0, otrzymano {kwota}")

    #     try:
    #         d = parse_date(data)
    #     except ValueError as e:
    #         message = f"data {data} format is incorrect, try YYYY-MM-DD"
    #         raise ValidationError(message) from e

    #     self.sklep = sklep
    #     self.kwota = kwota
    #     self.kategoria = kategoria
    #     self.data = d.isoformat()

    # def to_dict(self) -> dict:
    #     data: dict = {
    #         "sklep": self.sklep,
    #         "kwota": self.kwota,
    #         "kategoria": self.kategoria,
    #         "data": self.data,
    #     }

    #     return data

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Transaction":
        return cls(
            sklep=d["sklep"],
            kwota=d["kwota"],
            kategoria=d["kategoria"],
            data=d["data"]
        )
    
    # def __repr__(self):
    #    return f"Transaction(sklep={self.sklep!r}, kwota={self.kwota}, kategoria={self.kategoria!r}, data={self.data!r})"

    def __str__(self) -> str:
        return f"{self.data} | {self.sklep:<10} | {self.kwota:>7.2f} zł | {self.kategoria}"

