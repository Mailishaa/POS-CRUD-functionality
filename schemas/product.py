from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    barcode: str
    item_name: str
    # category_id: int
    category_id: int = 1

    cost_price: Decimal
    selling_price: Decimal
    stock_quantity: Decimal = Decimal("0.00")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    barcode: str = None
    item_name: str = None
    category_id: int = None
    cost_price: Decimal = None
    selling_price: Decimal = None    
    stock_quantity: Decimal = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    created_at: datetime

