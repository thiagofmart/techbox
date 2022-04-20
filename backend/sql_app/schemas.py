from datetime import datetime, date
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional


################################################################################
##### METHODS
# Client
class ClientBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    birth_date: datetime

class ClientCreate(ClientBase):
    password: str
class ClientRead(BaseModel):
    by: str
    parameter: str | int | float | date
class ClientUpdate(ClientBase):
    id: int
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    password: Optional[str]
    last_updated: datetime = datetime.now()
    confirming_password: str
class ClientDelete(BaseModel):
    id: int
    confirming_password: str

class Client(ClientBase):
    id: int

    class Config:
        orm_mode=True

# Address

class AddressBase(BaseModel):
    postal_code: str
    street: str
    district: str
    city: str
    state: str

class AddressCreate(AddressBase):
    number: str
    complement: str | None = None
    tag: str
    client_id: int
class AddressRead(BaseModel):
    by: str
    parameter:  str | int | float
class AddressUpdate(AddressBase):
    id: int
    postal_code: Optional[str]
    street: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    tag: Optional[str]
    
class AddressDelete(BaseModel):
    id: int

class Address(AddressBase):
    id: int
    number: str
    complement: str | None = None
    tag: str
    client_id: int
    class Config:
        orm_mode=True

################################################################################

class SessionData(BaseModel):
    id: int
    email: str
    user: str
    password: str
