from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from .database import Base, engine


class Planos(Base):
    __tablename__='planos'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    m_value = Column(Float)
    t_value = Column(Float)
    s_value = Column(Float)
    y_value = Column(Float)

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(EmailType, unique=True)
    hashed_password = Column(String)
    adressess = relationship('Address', backref='address', cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    client_id = Column(Integer, ForeignKey('client.id'))


database = {
'planos':['padrão',],
}
