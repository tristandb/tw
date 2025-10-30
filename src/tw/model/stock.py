from typing import Optional

from sqlmodel import Field, SQLModel


class StockBase(SQLModel):
    ticker: str = Field(index=True, unique=True, max_length=12)
    name: Optional[str] = Field(default=None, max_length=255)
    exchange: Optional[str] = Field(default=None, max_length=32)


class Stock(StockBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class StockCreate(StockBase):
    pass


class StockRead(StockBase):
    id: int

