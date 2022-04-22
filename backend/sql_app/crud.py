from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy.sql import update
from . import models, schemas, tools
import json


################################################################################
# CREATE
async def create_user(db: Session, content: schemas.UserCreate):
    hashed_password = tools.encrypt_pass(content.password)
    db_user = models.User(name=content.name, email=content.email, tag=content.tag, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
async def create_address(db: Session, content: schemas.AddressCreate):
    db_address = models.Address(postal_code=content.postal_code, street=content.street, number=content.number, complement=content.complement, district=content.district, city=content.city, state=content.state, tag=content.tag, user_id=content.user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
async def create_credit_card(db: Session, content: schemas.CreditCardCreate):
    db_credit_card = models.CreditCard(holder=content.holder, cardnumber=content.cardnumber, expirationdate=content.expirationdate, securitycode=content.securitycode, user_id=content.user_id)
    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    return db_credit_card
################################################################################
# READ
async def read_user(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'id':
            return db.query(models.User).filter(models.User.id==parameter).all()
        case 'email':
            return db.query(models.User).filter(models.User.email==parameter).all()
        case 'name':
            return db.query(models.User).filter(models.User.name==parameter).all()
        case 'tag':
            return db.query(models.User).filter(models.User.tag==parameter).all()
        case _:
            return []
async def read_address(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'id':
            return db.query(models.Address).filter(models.Address.id==parameter).all()
        case 'postal_code':
            return db.query(models.Address).filter(models.Address.postal_code==parameter).all()
        case 'street':
            return db.query(models.Address).filter(models.Address.street==parameter).all()
        case 'number':
            return db.query(models.Address).filter(models.Address.number==parameter).all()
        case 'complement':
            return db.query(models.Address).filter(models.Address.complement==parameter).all()
        case 'district':
            return db.query(models.Address).filter(models.Address.district==parameter).all()
        case 'city':
            return db.query(models.Address).filter(models.Address.city==parameter).all()
        case 'state':
            return db.query(models.Address).filter(models.Address.state==parameter).all()
        case 'tag':
            return db.query(models.Address).filter(models.Address.tag==parameter).all()
        case 'user_id':
            return db.query(models.Address).filter(models.Address.user_id==parameter).all()
        case _:
            return []
async def read_credit_card(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'holder':
            return db.query(models.CreditCard).filter(models.CreditCard.holder==parameter).all()
        case 'cardnumber':
            return db.query(models.CreditCard).filter(models.CreditCard.cardnumber==parameter).all()
        case 'expirationdate':
            return db.query(models.CreditCard).filter(models.CreditCard.expirationdate==parameter).all()
        case 'securitycode':
            return db.query(models.CreditCard).filter(models.CreditCard.securitycode==parameter).all()
        case _:
            return []

async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()
def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id==id).first()
def get_address_by_id(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id==id).first()
def get_credit_card_by_id(db: Session, id: int):
    return db.query(models.CreditCard).filter(models.CreditCard.id==id).first()


################################################################################
# UPSERT
async def update_user(db: Session, content: schemas.UserUpdate):
    content_dict = content.dict()
    if content_dict['password']:
        content_dict['hashed_password'] = tools.encrypt_pass(content_dict['password'])
    del content_dict['confirming_password'], content_dict['id'], content_dict['password']
    content_dict['last_updated'] = datetime.now()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_user = db.query(models.User).filter(models.User.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_user
async def update_address(db: Session, content: schemas.AddressUpdate):
    content_dict = content.dict()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_address = db.query(models.Address).filter(models.Address.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_address
async def update_credit_card(db: Session, content: schemas.CreditCardUpdate):
    content_dict = content.dict()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_credit_card = db.query(models.CreditCard).filter(models.CreditCard.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_credit_card

################################################################################
# DELETE
async def delete_user(db: Session, content: schemas.UserDelete):
    db_user = db.query(models.User).filter(models.User.id==content.id).first()
    db.delete(db_user)
    db.commit()
    return []
async def delete_address(db: Session, content: schemas.AddressDelete):
    db_address = db.query(models.Address).filter(models.Address.id==content.id).first()
    db.delete(db_address)
    db.commit()
    return []
async def delete_credit_card(db: Session, content: schemas.CreditCardDelete):
    db_credit_card = db.query(models.CreditCard).filter(models.CreditCard.id==content.id).first()
    db.delete(db_credit_card)
    db.commit()
    return []
