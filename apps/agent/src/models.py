"""SQLModel database schemas for the agent application."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class ProductPrice(SQLModel, table=True):
    __tablename__ = "product_prices"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str = Field(unique=True, index=True)
    product_name: str = Field(index=True)
    brand: Optional[str] = None
    category: Optional[str] = Field(default=None, index=True)
    price_lps: float
    list_price_lps: Optional[float] = None
    available_quantity: int = 0
    supermarket: str = Field(default="Paiz")
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
