from hashlib import pbkdf2_hmac

SALT = b'MATHEUSSAMUELTHIAGO'*2
KEY='38333295000'
SECRET='fed2163e2e8dccb53ff914ce9e2f1258'


def encrypt_pass(password):
    return pbkdf2_hmac('sha256', password.encode(), SALT, 500000).hex()
