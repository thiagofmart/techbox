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
async def create_plan(db: Session, content: schemas.PlanCreate):
    db_plan = models.Plan(desc=content.desc, m_value=content.m_value, t_value=content.t_value, s_value=content.s_value, y_value=content.y_value)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
async def create_contract(db: Session, content: schemas.PlanCreate):
    db_contract = models.Contracts(confirming_email_id=content.confirming_email_id,
                        freight=content.freight, user_id=content.user_id, creditcard_id=content.creditcard_id,
                        plan_id=content.plan_id, address_id=content.address_id)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
async def create_email(db: Session, content: schemas.EmailCreate):
    db_email = models.Emails(type=content.type, user_id=content.user_id)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email
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
async def read_plan(db: Session, by: str, parameter: str|int|float):
    match by:
        case 'm_value':
            return db.query(models.Plans).filter(models.Plans.m_value==parameter).all()
        case 't_value':
            return db.query(models.Plans).filter(models.Plans.t_value==parameter).all()
        case 's_value':
            return db.query(models.Plans).filter(models.Plans.s_value==parameter).all()
        case 'y_value':
            return db.query(models.Plans).filter(models.Plans.y_value==parameter).all()
        case _:
            return []

def get_user_by_email(db: Session, email: str):
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
async def update_credit_card(db: Session, content: schemas.CreditCardUpdate):
    content_dict = content.dict()
    content_dict = dict((k, v) for k, v in content_dict.items() if v is not None)
    db_plan = db.query(models.Plan).filter(models.Plan.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_plan

################################################################################
# DELETE
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
async def delete_plan(db: Session, content: schemas.CreditCardDelete):
    db_plan = db.query(models.Plan).filter(models.Plan.id==content.id).first()
    db.delete(db_plan)
    db.commit()
    return []
