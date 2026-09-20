from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    category_name: str
    description: str | None = None
    parent_category_id: int | None = None

    tax_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
    )

    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: str | None = None
    description: str | None = None
    parent_category_id: int | None = None

    tax_rate: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    is_active: bool | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="category_id",
        serialization_alias="id",
    )