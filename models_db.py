from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

class TransactionModel(Base):
    __tablename__ = "transactions"

    id:        Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    sklep:     Mapped[str]   = mapped_column(String, nullable=False)
    kwota:     Mapped[float] = mapped_column(Float, nullable=False)
    kategoria: Mapped[str]   = mapped_column(String, nullable=False)
    data:      Mapped[str]   = mapped_column(String, nullable=False)
    notatka:   Mapped[str]   = mapped_column(String, nullable=True, default=None)