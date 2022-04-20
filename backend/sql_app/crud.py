from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.sql import update
from . import models, schemas, tools
import json


################################################################################
# CREATE
async def create_client(db: Session, content: schemas.ClientCreate):
    hashed_password = tools.encrypt_pass(content.password)
    db_client = models.Client(first_name=content.first_name, last_name=content.last_name, email=content.email, birth_date=content.birth_date, hashed_password=hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

async def create_address(db: Session, content: schemas.AddressCreate):
    db_address = models.Address(postal_code=content.postal_code, street=content.street, number=content.number, complement=content.complement, district=content.district, city=content.city, state=content.state, tag=content.tag, client_id=content.client_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address
################################################################################
# READ
async def read_client(db: Session, by: str, parameter: str|int|float|date):
    match by:
        case 'id':
            return db.query(models.Client).filter(models.Client.id==parameter).all()
        case 'email':
            return db.query(models.Client).filter(models.Client.email==parameter).all()
        case 'first_name':
            return db.query(models.Client).filter(models.Client.first_name==parameter).all()
        case 'last_name':
            return db.query(models.Client).filter(models.Client.last_name==parameter).all()
        case 'birth_date':
            return db.query(models.Client).filter(models.Client.birth_date==parameter).all()
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
        case 'client_id':
            return db.query(models.Address).filter(models.Address.client_id==parameter).all()
        case _:
            return []

async def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email==email).first()
def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id==id).first()
def get_address_by_id(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id==id).first()

################################################################################
# UPSERT
async def update_client(db: Session, content: schemas.ClientUpdate):
    content_dict = content.dict()
    if content_dict['password']:
        content_dict['hashed_password'] = tools.encrypt_pass(content_dict['password'])
    del content_dict['confirming_password'], content_dict['id'], content_dict['password']

    db_client = db.query(models.Client).filter(models.Client.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_client
async def update_address(db: Session, content: schemas.AddressUpdate):
    content_dict = content.dict()
    db_address = db.query(models.Address).filter(models.Address.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_address

################################################################################
# DELETE
async def delete_client(db: Session, content: schemas.ClientDelete):
    db_client = db.query(models.Client).filter(models.Client.id==content.id).first()
    db.delete(db_client)
    db.commit()
    return []
async def delete_address(db: Session, content: schemas.AddressDelete):
    db_address = db.query(models.Address).filter(models.Address.id==content.id).first()
    db.delete(db_address)
    db.commit()
    return []
