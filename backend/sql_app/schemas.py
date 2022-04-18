from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional

class Address(BaseModel):
    id: int
    desc: str
    client_id: int
    class Config:
        orm_mode=True
################################################################################
# Métodos
class ClientBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    birth_date: datetime

class ClientCreate(ClientBase):
    password: str
class ClientRead(BaseModel):
    by: str
    parameter: str | int | float
class ClientUpdate(ClientBase):
    id: int
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[datetime]
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

################################################################################

class SessionData(BaseModel):
    id: int
    email: str
    user: str
    password: str
