from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class SaleBase(BaseModel):
    transaction_number: str
    user_id: int
    customer_id: int
    terminal_id: str
    subtotal: float
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float
    payment_method: str
    status: str = "Completed"

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    transaction_number: Optional[str] = None
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    terminal_id: Optional[str] = None
    subtotal: Optional[float] = None
    discount_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None

class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    created_at: datetime
