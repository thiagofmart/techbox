from datetime import datetime, date
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional


################################################################################
##### METHODS
# User
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    tag: str
class UserRead(BaseModel):
    by: str
    parameter: str | int | float | date
class UserUpdate(UserBase):
    id: int
    email: Optional[EmailStr]
    name: Optional[str]
    password: Optional[str]
    tag: Optional[str]
    confirming_password: str
class UserDelete(BaseModel):
    id: int
    confirming_password: str

class User(UserBase):
    id: int
    tag: str

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
    user_id: int
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
    user_id: int
    class Config:
        orm_mode=True

# Crédit Card
class CreditCardBase(BaseModel):
    holder: str
    cardnumber: str
    expirationdate: str
    securitycode: str

class CreditCardCreate(CreditCardBase):
    user_id: int
class CreditCardRead(BaseModel):
    by: str
    parameter: str|int|float
class CreditCardUpdate(CreditCardBase):
    id: int
    holder: Optional[str]
    cardnumber: Optional[str]
    expirationdate: Optional[str] # MM/YYYY
    securitycode: Optional[str]
class CreditCardDelete(BaseModel):
    id: str

class CreditCard(CreditCardBase):
    id: int

    class Config:
        orm_mode=True

################################################################################

class SessionData(BaseModel):
    id: int
    email: str
    user: str
    password: str
