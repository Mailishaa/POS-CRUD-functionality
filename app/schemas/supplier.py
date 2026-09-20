from datetime import datetime
from typing import Optional

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
)


class SupplierBase(BaseModel):
    supplier_name: str
    contact_name: Optional[str] = None

    phone: str = Field(
        validation_alias=AliasChoices(
            "phone",
            "phone_number",
        ),
    )

    email: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    lead_time_days: Optional[int] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_name: Optional[str] = None

    phone: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "phone",
            "phone_number",
        ),
    )

    email: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    lead_time_days: Optional[int] = None
    is_active: Optional[bool] = None


class SupplierRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="supplier_id",
        serialization_alias="id",
    )

    supplier_name: str
    contact_name: Optional[str] = None

    phone: str = Field(
        validation_alias="phone_number",
        serialization_alias="phone",
    )

    email: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    lead_time_days: Optional[int] = None
    is_active: bool

    created_at: datetime