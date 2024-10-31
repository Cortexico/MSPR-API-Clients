from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(BaseModel):
    name: str
    email: str
    address: str

class CustomerUpdate(CustomerBase):
    pass

class Customer(BaseModel):
    id: int
    name: str
    email: str
    address: str

    class Config:
        from_attributes = True  # Pour Pydantic v2