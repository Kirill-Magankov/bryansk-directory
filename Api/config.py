import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASS = os.getenv('MYSQL_PASS')
    DATABASE_URI = os.getenv('DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{DATABASE_URI}'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///database.db'

    API_VERSION = '0.1'
    API_TITLE = 'Справочник города Брянска'
    API_DESCRIPTION = 'API документация для проекта "Справочник города Брянска"'
    API_URL = '/api/v1'
