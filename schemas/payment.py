from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class PaymentBase(BaseModel):
    sale_id: int
    payment_method: str
    amount_tendered: Decimal
    amount_returned: Decimal = Decimal("0.00")
    gateway_reference: str = None
    status: str = "Approved"

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    sale_id: int = None
    payment_method: str = None
    amount_tendered: Decimal = None
    amount_returned: Decimal = None
    gateway_reference: str = None
    status: str = None

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    payment_datetime: datetime
