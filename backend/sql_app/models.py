from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from .database import Base, engine


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True)
    name = Column(String)
    tag = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    status = Column(Boolean, default=True) # ATIVO INATIVO

    adressess = relationship('Addressess', backref='users', cascade="all, delete-orphan")
    credit_cards = relationship('CreditCards', backref='users', cascade="all, delete-orphan")
    contracts = relationship('Contracts', backref='users')

class Addressess(Base):
    __tablename__ = 'addressess'
    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(String[8])
    street = Column(String)
    number = Column(String)
    complement = Column(String, nullable=True)
    district = Column(String)
    city = Column(String)
    state = Column(String)
    tag = Column(String) #entrega ou cobranca
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    contracts = relationship('Contracts', backref='addressess')

class CreditCards(Base):
    __tablename__ = 'creditcards'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    holder = Column(String)
    cardnumber = Column(String)
    expirationdate = Column(String)
    securitycode = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    contracts = relationship('Contracts', backref='contracts')

class Plans(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    m_value = Column(Float)
    t_value = Column(Float)
    s_value = Column(Float)
    y_value = Column(Float)

    contracts = relationship('Contracts', backref='plans')

class Contracts(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True, index=True)
    freight = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    creditcard_id = Column(Integer, ForeignKey('creditcards.id'))
    plan_id = Column(Integer, ForeignKey('plans.id'))
    address_id = Column(Integer, ForeignKey('addressess.id'))
    confirming_email_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
