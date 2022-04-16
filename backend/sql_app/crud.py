from sqlalchemy.orm import Session
from sqlalchemy.sql import update
from . import models, schemas, tools


################################################################################
# CREATE

def create_client(db: Session, content: schemas.ClientCreate):
    hashed_password = tools.encrypt_pass(content.password)
    db_client = models.Client(first_name=content.first_name, last_name=content.last_name, email=content.email, hashed_password=hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client



################################################################################
# READ
def read_client(db: Session, by: str, parameter: str|int|float):
    match by:
        case 'id':
            return db.query(models.Client).filter(models.Client.id==parameter).all()
        case 'email':
            return db.query(models.Client).filter(models.Client.email==parameter).all()
        case 'first_name':
            return db.query(models.Client).filter(models.Client.first_name==parameter).all()
        case 'last_name':
            return db.query(models.Client).filter(models.Client.last_name==parameter).all()
        case _:
            return []

def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email==email).first()
def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id==id).first()

################################################################################
# UPSERT
def update_client(db: Session, content: schemas.ClientUpdate):
    content_dict = content.dict()
    if content_dict['password']:
        content_dict['hashed_password'] = tools.encrypt_pass(content_dict['password'])
    del content_dict['confirming_password'], content_dict['id'], content_dict['password']

    db_client = db.query(models.Client).filter(models.Client.id==content.id).update(content_dict, synchronize_session=False)
    db.commit()
    return db_client #db_client


################################################################################
# DELETE
def delete_client(db: Session, content: schemas.ClientDelete):
    db_client = db.query(models.Client).filter(models.Client.id==content.id).first()
    db.delete(db_client)
    db.commit()
    return []
