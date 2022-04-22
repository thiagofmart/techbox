from uuid import UUID, uuid4
import jwt
import json
from sql_app import models, crud, schemas, tools
from sql_app.database import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pycep_correios


JWT_SECRET = 'MYJWTSECRET'
oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/v1/user/generate-token')
def _config_CORS(app):

    origins = [
        "http://localhost:8080",
        "http://localhost:3000",
    ]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

async def authenticate_user(email: str, password: str, db: Session = Depends(tools.get_db)):
    db_user = await crud.get_user_by_email(db=db, email=email)
    if not db_user:
        return False
    if not tools.verify_password(password, db_user):
        return False
    return db_user

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(json.loads(user_obj.json()), JWT_SECRET)
    return dict(access_token=token, token_type='bearer')

async def get_current_user(token: str = Depends(oauth2schema), db: Session=Depends(tools.get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = db.query(models.User).get(payload['id'])#await crud.get_user_by_id(db=db, id=int(ayload['id']))
    except:
        raise HTTPException(status_code=401, detail=f"Invalid Email or Password")
    return schemas.User.from_orm(user)

async def get_postal_code(postal_code: str):
    try:
        endereco = pycep_correios.get_address_from_cep(postal_code)
    except (pycep_correios.exceptions.InvalidCEP, pycep_correios.exceptions.BaseException):
        raise HTTPException(status_code=400, detail='CEP Inválido')
    except pycep_correios.exceptions.CEPNotFound:
        raise HTTPException(status_code=400, detail='CEP não encontrado')
    return endereco
