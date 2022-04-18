from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sql_app.database import Session
from sql_app import models, crud, schemas, tools
from uuid import UUID, uuid4
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi.middleware.cors import CORSMiddleware
import jwt
import json




tools.create_database()
app = FastAPI()
oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/v1/client/token')
origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]
#app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def validate_type(_object, _type):
    if type(_object)!=_type:
        raise HTTPException(status_code=400, detail=f"Wrong content Type {type(_object)}")

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

async def authenticate_client(email: str, password: str, db: Session = Depends(get_db)):
    db_client = await crud.get_client_by_email(db=db, email=email)
    if not db_client:
        return False
    if not tools.verify_password(password, db_client):
        return False
    return db_client

async def create_token(client: models.Client):
    client_obj = schemas.Client.from_orm(client)
    token = jwt.encode(json.loads(client_obj.json()), tools.JWT_SECRET)
    return dict(access_token=token, token_type='bearer')

async def get_current_client(token: str = Depends(oauth2schema), db: Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, tools.JWT_SECRET, algorithms=['HS256'])
        client = db.query(models.Client).get(payload['id'])#await crud.get_client_by_id(db=db, id=int(ayload['id']))
    except:
        raise HTTPException(status_code=401, detail=f"Invalid Email or Password")
    return schemas.Client.from_orm(client)

@app.get('/', response_class=HTMLResponse)
async def homepage():
    return '<h1>HOME PAGE</h1>'

@app.post('/api/v1/client/create', response_model=schemas.Client)
async def client_create(payload: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = await crud.get_client_by_email(db, payload.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_client(db=db, content=payload)

@app.post('/api/v1/client/read', response_model=list[schemas.Client]|list)
async def client_read(payload: schemas.ClientRead, db: Session = Depends(get_db)):
        return await crud.read_client(db=db, by=payload.by, parameter=payload.parameter)

@app.post('/api/v1/client/update', response_model=schemas.Client|list[schemas.Client]|list)
async def client_update(payload: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = await crud.get_client_by_id(db=db, id=payload.id)
    if not db_client:
        raise HTTPException(status_code=400, detail=f"Client with ID: {payload.id} isn't registered")
    if not tools.verify_password(payload.confirming_password, db_client):
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    return await crud.update_client(db=db, content=payload)

@app.post('/api/v1/client/delete', response_model=schemas.Client|list[schemas.Client]|list)
async def client_delete(payload: schemas.ClientDelete, db: Session = Depends(get_db)):
    db_client = await crud.get_client_by_id(db=db, id=payload.id)
    if not db_client:
        raise HTTPException(status_code=400, detail=f"Client with ID: {payload.id} isn't registered")
    if not tools.verify_password(payload.confirming_password, db_client):
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    return await crud.delete_client(db=db, content=payload)

@app.post('/api/v1/client/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client = await authenticate_client(email=form_data.username, password=form_data.password, db=db)
    if not client:
        raise HTTPException(status_code=401, detail='Invalid Credentials')
    return await create_token(client)

@app.post('/api/v1/client/me', response_model=schemas.Client)
async def get_client(client: schemas.Client = Depends(get_current_client)):
    return client
