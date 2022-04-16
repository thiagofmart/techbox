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
    password: Optional[str]
    confirming_password: str
class ClientDelete(BaseModel):
    id: int
    confirming_password: str

class Client(ClientBase):
    id: int
    addressess: list[Address] = []

    class Config:
        orm_mode=True

class CallClient(BaseModel):
    #key: str
    #secret: str
    content: ClientUpdate | ClientCreate | ClientRead | ClientDelete
