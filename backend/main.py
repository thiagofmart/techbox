from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sql_app.database import Session, engine
from sql_app import models, crud, schemas, tools


models.Base.metadata.create_all(engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
def validate_type(_object, _type):
    if type(_object)!=_type:
        raise HTTPException(status_code=400, detail=f"Wrong content Type {type(_object)}")

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get('/', response_class=HTMLResponse)
async def homepage():
    return '<h1>HOME PAGE</h1>'


@app.get('/planos/{plano}', response_class=HTMLResponse)
async def principal(request: Request, plano: str):
    if plano in models.database['planos']:
        return templates.TemplateResponse('plano.html', {'request': request, 'plano':plano})
    else:
        return "<h1>PLANO NÃO ENCONTRADO</h1>"

@app.post('/api/v1/client/create', response_model=schemas.Client)
async def client_create(payload: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_email(db, payload.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_client(db=db, content=payload)

@app.post('/api/v1/client/read', response_model=schemas.Client|list[schemas.Client]|list)
async def client_read(payload: schemas.ClientRead, db: Session = Depends(get_db)):
        return crud.read_client(db=db, by=payload.by, parameter=payload.parameter)

@app.post('/api/v1/client/update', response_model=schemas.Client|list[schemas.Client]|list)
async def client_update(payload: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_id(db=db, id=payload.id)
    if not db_client:
        raise HTTPException(status_code=400, detail=f"Client with ID: {payload.id} isn't registered")
    if tools.encrypt_pass(payload.confirming_password)!=db_client.hashed_password:
        raise HTTPException(status_code=400, detail=f"Wrong confirming password")
    validate_type(payload, schemas.ClientUpdate)
    return crud.update_client(db=db, content=payload)

@app.post('/api/v1/client/delete', response_model=schemas.Client|list[schemas.Client]|list)
async def client_delete(payload: schemas.ClientDelete, db: Session = Depends(get_db)):
    return crud.delete_client(db=db, content=payload)
