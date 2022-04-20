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
oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/v1/client/generate-token')
def _config_CORS(app):

    origins = [
        "http://localhost:8080",
        "http://localhost:3000",
    ]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

async def authenticate_client(email: str, password: str, db: Session = Depends(tools.get_db)):
    db_client = await crud.get_client_by_email(db=db, email=email)
    if not db_client:
        return False
    if not tools.verify_password(password, db_client):
        return False
    return db_client

async def create_token(client: models.Client):
    client_obj = schemas.Client.from_orm(client)
    token = jwt.encode(json.loads(client_obj.json()), JWT_SECRET)
    return dict(access_token=token, token_type='bearer')

async def get_current_client(token: str = Depends(oauth2schema), db: Session=Depends(tools.get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        client = db.query(models.Client).get(payload['id'])#await crud.get_client_by_id(db=db, id=int(ayload['id']))
    except:
        raise HTTPException(status_code=401, detail=f"Invalid Email or Password")
    return schemas.Client.from_orm(client)

async def get_postal_code(postal_code: str):
    try:
        endereco = pycep_correios.get_address_from_cep(postal_code)
    except (pycep_correios.exceptions.InvalidCEP, pycep_correios.exceptions.BaseException):
        raise HTTPException(status_code=400, detail='CEP Inválido')
    except pycep_correios.exceptions.CEPNotFound:
        raise HTTPException(status_code=400, detail='CEP não encontrado')
    return endereco
