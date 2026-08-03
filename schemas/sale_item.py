from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class SaleItemBase(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    discount_applied: Decimal = Decimal("0.00")
    tax_amount: Decimal
    total_price: Decimal
    is_returned: bool = False

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemUpdate(BaseModel):
    sale_id: int = None
    product_id: int = None
    quantity: int = None
    unit_price: Decimal = None
    discount_applied: Decimal = None
    tax_amount: Decimal = None
    total_price: Decimal = None
    is_returned: bool = None

class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: int
