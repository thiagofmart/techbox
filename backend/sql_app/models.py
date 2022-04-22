from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date
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


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True)
    name = Column(String)
    tag = Column(String)
    hashed_password = Column(String)
    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)
    adressess = relationship('Address', backref='address', cascade="all, delete-orphan")
    credit_cards = relationship('CreditCard', backref='creditcard', cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(String[8])
    street = Column(String)
    number = Column(String)
    complement = Column(String, nullable=True)
    district = Column(String)
    city = Column(String)
    state = Column(String)
    tag = Column(String) #entrega ou cobranca
    user_id = Column(Integer, ForeignKey('user.id'))


class CreditCard(Base):
    __tablename__ = 'creditcard'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    holder = Column(String)
    cardnumber = Column(String)
    expirationdate = Column(String)
    securitycode = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
