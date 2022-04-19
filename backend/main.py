from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sql_app.database import Session
from sql_app import models, crud, schemas, tools
import utils


app = FastAPI()
tools._create_database()    #URL where token is generated
utils._config_CORS(app=app)


@app.get('/', response_class=HTMLResponse)
async def homepage():
    return '<h1>HOME PAGE</h1>'

@app.post('/api/v1/client/create', response_model=schemas.Client)
async def client_create(payload: schemas.ClientCreate, db: Session = Depends(tools.get_db)):
    db_client = await crud.get_client_by_email(db, payload.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_client(db=db, content=payload)

@app.post('/api/v1/client/read', response_model=list[schemas.Client]|list)
async def client_read(payload: schemas.ClientRead, db: Session = Depends(tools.get_db)):
    return await crud.read_client(db=db, by=payload.by, parameter=payload.parameter)

@app.post('/api/v1/client/update', response_model=schemas.Client|list[schemas.Client]|list)
async def client_update(payload: schemas.ClientUpdate, db: Session = Depends(tools.get_db)):
    db_client = crud.get_client_by_id(db=db, id=payload.id)
    if not db_client:
        raise HTTPException(status_code=400, detail=f"Client with ID: {payload.id} isn't registered")
    if not tools.verify_password(payload.confirming_password, db_client):
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    return await crud.update_client(db=db, content=payload)

@app.post('/api/v1/client/delete', response_model=schemas.Client|list[schemas.Client]|list)
async def client_delete(payload: schemas.ClientDelete, db: Session = Depends(tools.get_db)):
    db_client = crud.get_client_by_id(db=db, id=payload.id)
    if not db_client:
        raise HTTPException(status_code=400, detail=f"Client with ID: {payload.id} isn't registered")
    if not tools.verify_password(payload.confirming_password, db_client):
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    return await crud.delete_client(db=db, content=payload)


################################################################################
# SESSION
@app.post('/api/v1/client/generate-token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(tools.get_db)):
    client = await utils.authenticate_client(email=form_data.username, password=form_data.password, db=db)
    if not client:
        raise HTTPException(status_code=401, detail='Invalid Credentials')
    return await utils.create_token(client)

@app.post('/api/v1/client/validate-token', response_model=schemas.Client)
async def get_client(client: schemas.Client = Depends(utils.get_current_client)):
    return client

################################################################################
# ADDRESS
@app.post('/api/v1/address/consult-postal-code', response_model=schemas.AddressBase)
async def consult_postal_code(postal_code: str):
    endereco = await utils.get_postal_code(postal_code)
    address_obj = schemas.AddressBase(postal_code=endereco['cep'].replace('-', ''), street=endereco['logradouro'], district=endereco['bairro'], city=endereco['cidade'], state=endereco['uf'])
    return address_obj

@app.post('/api/v1/address/create', response_model=schemas.Address)
async def address_create(payload: schemas.AddressCreate, db: Session = Depends(tools.get_db)):
    cliend_db = crud.get_client_by_id(db=db, id=payload.client_id)
    if not cliend_db:
        raise HTTPException(status_code=400, detail=f'ID {payload.client_id} de cliente inexistente')
    return await crud.create_address(db=db, content=payload)
