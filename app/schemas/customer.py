from datetime import date
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    first_name: str
    last_name: str

    phone: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("phone", "phone_number"),
    )

    email: Optional[str] = None

    loyalty_points: int = Field(
        default=0,
        ge=0,
    )

    registration_date: date = Field(
        default_factory=date.today,
    )


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    phone: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("phone", "phone_number"),
    )

    email: Optional[str] = None

    loyalty_points: Optional[int] = Field(
        default=None,
        ge=0,
    )

    registration_date: Optional[date] = None


class CustomerRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="customer_id",
        serialization_alias="id",
    )

    first_name: str
    last_name: str

    phone: Optional[str] = Field(
        default=None,
        validation_alias="phone_number",
        serialization_alias="phone",
    )

    email: Optional[str] = None
    loyalty_points: int
    registration_date: date