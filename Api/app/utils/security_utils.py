from datetime import timedelta
from uuid import uuid4
from flask_jwt_extended import create_access_token
from app import bcrypt


def get_uuid(): return str(uuid4())


def password_hash_generate(password): return bcrypt.generate_password_hash(password).decode('utf8')


def password_hash_compare(password_hash, password): return bcrypt.check_password_hash(password_hash, password)


def create_dev_token(hours=12): return create_access_token(identity='developer', expires_delta=timedelta(hours=hours))
# def create_dev_token(hours=12): return create_access_token(identity=2, expires_delta=timedelta(hours=hours))
