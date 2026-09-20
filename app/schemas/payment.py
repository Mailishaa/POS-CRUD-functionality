from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    sale_id: int

    amount_paid: Decimal = Field(
        ge=0,
        validation_alias=AliasChoices(
            "amount_paid",
            "amount_tendered",
        ),
    )

    payment_method: str
    payment_status: str = "Completed"
    reference_number: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    sale_id: Optional[int] = None

    amount_paid: Optional[Decimal] = Field(
        default=None,
        ge=0,
        validation_alias=AliasChoices(
            "amount_paid",
            "amount_tendered",
        ),
    )

    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    reference_number: Optional[str] = None


class PaymentRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="payment_id",
        serialization_alias="id",
    )

    sale_id: int

    amount_paid: Decimal = Field(
        validation_alias="amount_tendered",
        serialization_alias="amount_paid",
    )

    payment_method: str
    payment_status: str
    reference_number: Optional[str] = None

    created_at: datetime = Field(
        validation_alias="payment_datetime",
        serialization_alias="created_at",
    )