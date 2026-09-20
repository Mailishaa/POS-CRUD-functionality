from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class ProductBase(BaseModel):
    barcode: Optional[str] = None

    product_name: str = Field(
        validation_alias=AliasChoices("product_name", "item_name")
    )

    unit_price: Decimal = Field(ge=0)

    stock_qty: int = Field(default=0, ge=0)

    category_id: Optional[int] = None

    supplier_id: Optional[int] = None

    is_active: bool = True


class ProductCreate(ProductBase):
    cost_price: Decimal = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    barcode: Optional[str] = None

    product_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("product_name", "item_name"),
    )

    unit_price: Optional[Decimal] = Field(default=None, ge=0)

    stock_qty: Optional[int] = Field(default=None, ge=0)

    category_id: Optional[int] = None

    supplier_id: Optional[int] = None

    cost_price: Optional[Decimal] = Field(default=None, ge=0)

    is_active: Optional[bool] = None


class ProductRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="product_id",
        serialization_alias="id",
    )

    barcode: Optional[str] = None

    product_name: str = Field(
        validation_alias="item_name",
        serialization_alias="product_name",
    )

    unit_price: Decimal = Field(
        validation_alias="selling_price",
        serialization_alias="unit_price",
    )

    stock_qty: int = Field(
        validation_alias="stock_quantity",
        serialization_alias="stock_qty",
    )

    category_id: Optional[int] = None

    supplier_id: Optional[int] = None

    is_active: bool

    cost_price: Decimal

    created_at: datetime