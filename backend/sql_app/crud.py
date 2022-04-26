from datetime import datetime, date
from .database import Session
from sqlalchemy.sql import update
from . import models, schemas, tools
import json


################################################################################
# CREATE
async def create_user(db: Session, content: schemas.UserCreate):
    hashed_password = tools.encrypt_pass(content.password)
    db_user = models.Users(name=content.name, email=content.email, tag=content.tag, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
async def create_address(db: Session, content: schemas.AddressCreate):
    db_address = models.Addressess(postal_code=content.postal_code, street=content.street, number=content.number, complement=content.complement, district=content.district, city=content.city, state=content.state, tag=content.tag, user_id=content.user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
async def create_credit_card(db: Session, content: schemas.CreditCardCreate):
    db_credit_card = models.CreditCards(holder=content.holder, cardnumber=content.cardnumber, expirationdate=content.expirationdate, securitycode=content.securitycode, user_id=content.user_id)
    db.add(db_credit_card)
    db.commit()
    db.refresh(db_credit_card)
    return db_credit_card
################################################################################
# READ
async def read_user(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'id':
            return db.query(models.Users).filter(models.Users.id==parameter).all()
        case 'email':
            return db.query(models.Users).filter(models.Users.email==parameter).all()
        case 'name':
            return db.query(models.Users).filter(models.Users.name==parameter).all()
        case 'tag':
            return db.query(models.Users).filter(models.Users.tag==parameter).all()
        case 'status':
            return db.query(models.Users).filter(models.Users.status==parameter).all()
        case _:
            return []
async def read_address(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'id':
            return db.query(models.Addressess).filter(models.Addressess.id==parameter).all()
        case 'postal_code':
            return db.query(models.Addressess).filter(models.Addressess.postal_code==parameter).all()
        case 'street':
            return db.query(models.Addressess).filter(models.Addressess.street==parameter).all()
        case 'number':
            return db.query(models.Addressess).filter(models.Addressess.number==parameter).all()
        case 'complement':
            return db.query(models.Addressess).filter(models.Addressess.complement==parameter).all()
        case 'district':
            return db.query(models.Addressess).filter(models.Addressess.district==parameter).all()
        case 'city':
            return db.query(models.Addressess).filter(models.Addressess.city==parameter).all()
        case 'state':
            return db.query(models.Addressess).filter(models.Addressess.state==parameter).all()
        case 'tag':
            return db.query(models.Addressess).filter(models.Addressess.tag==parameter).all()
        case 'user_id':
            return db.query(models.Addressess).filter(models.Addressess.user_id==parameter).all()
        case _:
            return []
async def read_credit_card(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'holder':
            return db.query(models.CreditCards).filter(models.CreditCards.holder==parameter).all()
        case 'cardnumber':
            return db.query(models.CreditCards).filter(models.CreditCards.cardnumber==parameter).all()
        case 'expirationdate':
            return db.query(models.CreditCards).filter(models.CreditCards.expirationdate==parameter).all()
        case 'securitycode':
            return db.query(models.CreditCards).filter(models.CreditCards.securitycode==parameter).all()
        case _:
            return []

async def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email==email).first()
def get_user_by_id(db: Session, id: int):
    return db.query(models.Users).filter(models.Users.id==id).first()
def get_address_by_id(db: Session, id: int):
    return db.query(models.Addressess).filter(models.Addressess.id==id).first()
def get_credit_card_by_id(db: Session, id: int):
    return db.query(models.CreditCards).filter(models.CreditCards.id==id).first()


################################################################################
# UPSERT
async def update_user(db: Session, content: schemas.UserUpdate):
    content_dict = content.dict()
    if content_dict['password']:
        content_dict['hashed_password'] = tools.encrypt_pass(content_dict['password'])
    del content_dict['confirming_password'], content_dict['id'], content_dict['password']
    content_dict['last_updated'] = datetime.now()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_user = db.query(models.Users).filter(models.Users.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_user
async def update_address(db: Session, content: schemas.AddressUpdate):
    content_dict = content.dict()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_address = db.query(models.Addressess).filter(models.Addressess.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_address
async def update_credit_card(db: Session, content: schemas.CreditCardUpdate):
    content_dict = content.dict()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_credit_card = db.query(models.CreditCards).filter(models.CreditCards.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_credit_card

################################################################################
# DELETE
async def delete_user(db: Session, content: schemas.UserDelete):
    db_user = db.query(models.Users).filter(models.Users.id==content.id).first()
    db.delete(db_user)
    db.commit()
    return []
async def delete_address(db: Session, content: schemas.AddressDelete):
    db_address = db.query(models.Addressess).filter(models.Addressess.id==content.id).first()
    db.delete(db_address)
    db.commit()
    return []
async def delete_credit_card(db: Session, content: schemas.CreditCardDelete):
    db_credit_card = db.query(models.CreditCards).filter(models.CreditCards.id==content.id).first()
    db.delete(db_credit_card)
    db.commit()
    return []
