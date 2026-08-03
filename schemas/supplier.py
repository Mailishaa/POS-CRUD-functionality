from pydantic import BaseModel, ConfigDict, EmailStr

class SupplierBase(BaseModel):
    supplier_name: str
    contact_name: str = None
    phone_number: str
    email: EmailStr = None
    address: str = None
    tax_id: str = None
    lead_time_days: int = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    supplier_name: str = None
    contact_name: str = None
    phone_number: str = None
    email: EmailStr = None
    address: str = None
    tax_id: str = None
    lead_time_days: int = None
    is_active: bool = None

class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
