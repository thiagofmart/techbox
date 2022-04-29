from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.security import OAuth2PasswordRequestForm
from sql_app.database import Session
from sql_app import crud, schemas, tools
import utils
import emails_templates


app = FastAPI()
tools._create_database()    #URL where token is generated
utils._config_CORS(app=app)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


#db = Session()
#utils.insert_plans(db)

@app.get('/', response_class=HTMLResponse)
async def homepage():
    return '<h1>HOME PAGE</h1>'

@app.post('/api/v1/user/create', response_model=schemas.User)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(tools.get_db)):
    db_user = crud.get_user_by_email(db, payload.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, content=payload)
@app.post('/api/v1/user/read', response_model=list[schemas.User]|list)
async def read_user(payload: schemas.UserRead, db: Session = Depends(tools.get_db)):
    return await crud.read_user(db=db, by=payload.by, parameter=payload.parameter)
@app.post('/api/v1/user/update', response_model=schemas.User)
async def update_user(payload: schemas.UserUpdate, db: Session = Depends(tools.get_db)):
    db_user = crud.get_user_by_id(db=db, id=payload.id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with ID: {payload.id} isn't registered")
    if not tools.verify_password(payload.confirming_password, db_user):
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    _ = await crud.update_user(db=db, content=payload)
    return db_user

################################################################################
# SESSION
@app.post('/api/v1/user/generate-token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(tools.get_db)):
    user = await utils.authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid Credentials')
    return await utils.create_token(user)
@app.post('/api/v1/user/validate-token', response_model=schemas.User)
async def get_user(user: schemas.User = Depends(utils.get_current_user)):
    return user
@app.get('/api/v1/user/current_user', response_model=schemas.User)
async def get_current_user(token: str = Depends(utils.oauth2schema), db: Session=Depends(tools.get_db)):
    return await utils.get_current_user(token=token, db=db)

################################################################################
# ADDRESS
@app.post('/api/v1/address/consult-postal-code', response_model=schemas.AddressBase)
async def consult_postal_code(postal_code: str):
    endereco = await utils.get_postal_code(postal_code)
    address_obj = schemas.AddressBase(postal_code=endereco['cep'].replace('-', ''), street=endereco['logradouro'], district=endereco['bairro'], city=endereco['cidade'], state=endereco['uf'])
    return address_obj
@app.post('/api/v1/address/create', response_model=schemas.Address)
async def create_address(payload: schemas.AddressCreate, db: Session = Depends(tools.get_db)):
    endereco = await utils.get_postal_code(payload.postal_code)
    cliend_db = crud.get_user_by_id(db=db, id=payload.user_id)
    if not cliend_db:
        raise HTTPException(status_code=400, detail=f'ID {payload.user_id} de usuario inexistente')
    return await crud.create_address(db=db, content=payload)
@app.post('/api/v1/address/read', response_model=list)
async def read_address(payload: schemas.AddressRead, db: Session = Depends(tools.get_db)):
    return await crud.read_address(db=db, by=payload.by, parameter=payload.parameter)
@app.post('/api/v1/address/update', response_model=schemas.Address)
async def update_address(payload: schemas.AddressUpdate, db: Session = Depends(tools.get_db)):
    db_address = crud.get_address_by_id(db=db, id=payload.id)
    if not db_address:
        raise HTTPException(status_code=400, detail=f"Address with ID: {payload.id} isn't registered")
    _ = await crud.update_address(db=db, content=payload)
    return db_address
@app.post('/api/v1/address/delete', response_model=list)
async def delete_address(payload: schemas.AddressDelete, db: Session = Depends(tools.get_db)):
    db_address = crud.get_address_by_id(db=db, id=payload.id)
    if not db_address:
        raise HTTPException(status_code=400, detail=f"Address with ID: {payload.id} isn't registered")
    return await crud.delete_address(db=db, content=payload)

################################################################################
# CREDIT CARD

@app.post('/api/v1/credit-card/create', response_model=schemas.CreditCard)
async def create_credit_card(payload: schemas.CreditCardCreate, db: Session = Depends(tools.get_db)):
    return await crud.create_credit_card(db=db, content=payload)
@app.post('/api/v1/credit-card/read', response_model=list)
async def read_credit_card(payload: schemas.CreditCardRead, db: Session = Depends(tools.get_db)):
    return await crud.read_credit_card(db=db, by=payload.by, parameter=payload.parameter)
@app.post('/api/v1/credit-card/update', response_model=schemas.CreditCard)
async def update_credit_card(payload: schemas.CreditCardUpdate, db: Session = Depends(tools.get_db)):
    db_credit_card = crud.get_credit_card_by_id(db=db, id=payload.id)
    if not db_credit_card:
        raise HTTPException(status_code=400, detail=f"Credit Card with ID: {payload.id} isn't registered")
    _ = await crud.update_credit_card(db=db, content=payload)
    return db_credit_card
@app.post('/api/v1/credit-card/delete', response_model=list)
async def delete_credit_card(payload: schemas.CreditCardDelete, db: Session = Depends(tools.get_db)):
    db_credit_card = crud.get_credit_card_by_id(db=db, id=payload.id)
    if not db_credit_card:
        raise HTTPException(status_code=400, detail=f"Credit Card with ID: {payload.id} isn't registered")
    return await crud.delete_credit_card(db=db, content=payload)

################################################################################
# PLANS
@app.post('/api/v1/plan/create', response_model=schemas.Plan)
async def create_plan(payload: schemas.PlanCreate, db: Session = Depends(tools.get_db)):
    return await crud.create_plan(db=db, content=payload)
@app.post('/api/v1/plan/read', response_model=list)
async def read_plan(payload: schemas.PlanRead, db: Session = Depends(tools.get_db)):
    return await crud.read_plan(db=db, by=payload.by, parameter=payload.parameter)
@app.post('/api/v1/plan/update', response_model=schemas.Plan)
async def update_plan(payloda: schemas.PlanUpdate, db: Session = Depends(tools.get_db)):
    return await crud.update_plan(db=db, content=payload)

################################################################################
# CONTRACTS
@app.post('/api/v1/confirming_email')
@limiter.limit('1/2minute')
async def send_confirming_email(request: Request, receiver: str):
    receivers = [receiver, 'devloot2@gmail.com']
    emails_templates.TEST_confirming_email(receivers=receivers)
    utils.logger.log('INFO', 'Confirming e-mail sended!')
    return {'email_id':123, 'email_code': 456789}
@app.post('/api/v1/contract/create')
async def create_contract(payload: schemas.ContractCreate, db: Session = Depends(tools.get_db)):
    db_user = tools.get_user_by_id(db=db, id=payload.user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with ID: {payload.id} isn't registered")

    return await crud.create_contract(db=db, content=payload)
@app.post('/api/v1/contract/read', response_model=list)
async def read_contract(payload: schemas.ContractRead, db: Session = Depends(tools.get_db)):
    return await crud.read_contract(db=db, by=payload.by, parameter=payload.parameter)
