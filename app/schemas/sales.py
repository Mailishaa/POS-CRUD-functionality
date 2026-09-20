from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SaleBase(BaseModel):
    transaction_number: Optional[str] = None

    user_id: int = 1

    customer_id: int = 1

    terminal_id: str = "MAIN"

    subtotal: Optional[Decimal] = None

    discount_amount: Decimal = Field(default=0, ge=0)

    tax_amount: Decimal = Field(default=0, ge=0)

    total_amount: Decimal = Field(ge=0)

    payment_method: str = "Cash"

    status: str = "Completed"


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    transaction_number: Optional[str] = None
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    terminal_id: Optional[str] = None
    subtotal: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = Field(default=None, ge=0)
    tax_amount: Optional[Decimal] = Field(default=None, ge=0)
    total_amount: Optional[Decimal] = Field(default=None, ge=0)
    payment_method: Optional[str] = None
    status: Optional[str] = None


class SaleRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="sale_id",
        serialization_alias="id",
    )

    transaction_number: str
    user_id: int
    customer_id: int
    terminal_id: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    payment_method: str
    status: str
    created_at: datetime