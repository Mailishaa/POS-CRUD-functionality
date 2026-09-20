from decimal import Decimal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
)


class SaleItemBase(BaseModel):
    sale_id: int = Field(
        validation_alias=AliasChoices(
            "sale_id",
            "Sale_id",
        )
    )

    product_id: int = Field(
        validation_alias=AliasChoices(
            "product_id",
            "Product_id",
        )
    )

    quantity: int = Field(
        gt=0
    )

    item_price: Decimal = Field(
        validation_alias=AliasChoices(
            "item_price",
            "unit_price",
        ),
        gt=0,
    )

    discount_applied: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    total_price: Decimal | None = None

    is_returned: bool = False


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    sale_id: int | None = None
    product_id: int | None = None

    quantity: int | None = Field(
        default=None,
        gt=0,
    )

    item_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    discount_applied: Decimal | None = None
    tax_amount: Decimal | None = None
    total_price: Decimal | None = None
    is_returned: bool | None = None


class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="sale_item_id",
        serialization_alias="id",
    )