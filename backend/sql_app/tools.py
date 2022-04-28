from hashlib import pbkdf2_hmac
from .models import Base
from .database import engine, Session


SALT = b'MATHEUSSAMUELTHIAGO'*2
KEY='38333295000'
SECRET='fed2163e2e8dccb53ff914ce9e2f1258'


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def _create_database():
    Base.metadata.create_all(engine)
def encrypt_pass(password):
    return pbkdf2_hmac('sha256', password.encode(), SALT, 500000).hex()
def verify_password(password, db_client):
    return encrypt_pass(password)==db_client.hashed_password
