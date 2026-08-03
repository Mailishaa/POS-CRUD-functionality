from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ReceiptBase(BaseModel):
    sale_id: int
    receipt_type: str

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptUpdate(BaseModel):
    sale_id: int = None
    receipt_type: str = None

class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: int
    issued_datetime: datetime
