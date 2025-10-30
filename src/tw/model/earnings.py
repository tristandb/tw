"""Models for earnings call data."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, ForeignKey


class EarningsCall(SQLModel, table=True):
    """Represents an earnings call transcript for a stock."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_id: int = Field(foreign_key="stock.id", index=True)
    date: datetime = Field(index=True)
    quarter: str = Field(max_length=6)  # Format: 2025Q4
    fiscal_year: int = Field(index=True)
    fiscal_quarter: int = Field(index=True)
    title: str
    content: str
    source_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "stock_id": 1,
                "date": "2025-10-30T16:00:00Z",
                "quarter": "2025Q4",
                "fiscal_year": 2025,
                "fiscal_quarter": 4,
                "title": "Apple Inc. (AAPL) Q4 2025 Earnings Call Transcript",
                "content": "Good afternoon and thank you for joining us...",
                "source_url": "https://seekingalpha.com/article/...",
            }
        }