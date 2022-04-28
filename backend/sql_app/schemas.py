from datetime import datetime, date
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional


################################################################################
##### METHODS
# User
class UserBase(BaseModel):
    email: EmailStr
    name: str
    tag: str

class UserCreate(UserBase):
    password: str
class UserRead(BaseModel):
    by: str
    parameter: str | int | float | date
class UserUpdate(UserBase):
    id: int
    email: Optional[EmailStr]
    name: Optional[str]
    password: Optional[str]
    tag: Optional[str]
    status: Optional[bool]
    confirming_password: str
class UserDelete(BaseModel):
    id: int
    confirming_password: str

class User(UserBase):
    id: int
    status: bool


    class Config:
        orm_mode=True

# Address

class AddressBase(BaseModel):
    postal_code: str
    street: str
    district: str
    city: str
    state: str
class OptionalAddressBase(BaseModel):
    postal_code: Optional[str]
    street: Optional[str]
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]
    number: Optional[str]
    complement: Optional[str]


class AddressCreate(AddressBase):
    number: str
    complement: str | None = None
    tag: str
    user_id: int
class AddressRead(BaseModel):
    by: str
    parameter:  str | int | float
class AddressUpdate(OptionalAddressBase):
    id: int
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

# Plans
class PlanBase(BaseModel):
    desc: str
    m_value: str
    t_value: str
    s_value: str
    y_value: str

class PlanCreate(PlanBase):
    pass
class PlanRead(BaseModel):
    by: str
    parameter: str|int|float
class PlanUpdate(PlanBase):
    id: int|float
    desc: Optional[str]
    m_value: Optional[str]
    t_value: Optional[str]
    s_value: Optional[str]
    y_value: Optional[str]
class PlanDelete(BaseModel):
    id: int

class Plan(PlanBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode=True

# Contracts

class ContractBase(BaseModel):
    freight: float|int
    user_id: int|float
    creditcard: CreditCardBase
    plan_id: int|float
    delivery_address: AddressBase
    billing_address: AddressBase

class ContractCreate(ContractBase):
    confirming_email_id: int
class ContractRead(BaseModel):
    by: str
    parameter: str|int|float
class ContractUpdate(ContractBase):
    id: int
    delivery_address: Optional[AddressBase]
    billing_address: Optional[AddressBase]
    status: Optional[bool]

class Contract(PlanBase):
    id: int
    status: bool

    class Config:
        orm_mode=True

# Emails


class EmailCreate(BaseModel):
    pass
################################################################################

class SessionData(BaseModel):
    id: int
    email: str
    user: str
    password: str
