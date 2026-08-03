from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr

class CustomerBase(BaseModel):
    first_name: str
    last_name: str = None
    phone_number: str
    email: EmailStr = None
    loyalty_points: int = 0
    registration_date: date = date.today

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email: EmailStr = None
    loyalty_points: int = None
    registration_date: date = None

class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
