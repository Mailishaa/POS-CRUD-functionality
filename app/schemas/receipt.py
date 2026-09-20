from datetime import datetime

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
)


class ReceiptBase(BaseModel):
    sale_id: int = Field(
        validation_alias=AliasChoices(
            "sale_id",
            "Sale_id",
        )
    )

    receipt_number: str


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    sale_id: int | None = None
    receipt_number: str | None = None


class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(
        validation_alias="receipt_id",
        serialization_alias="id",
    )

    created_at: datetime = Field(
        validation_alias="issued_datetime",
        serialization_alias="created_at",
    )