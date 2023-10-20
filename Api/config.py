import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'secret_key'
    JWT_SECRET_KEY = 'jwt_secret_key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:toor@localhost/it_startup'

    API_VERSION = '0.1'
    API_TITLE = 'Справочник города Брянска'
    API_DESCRIPTION = 'API документация для проекта "Справочник города Брянска"'

    API_URL = '/api/v1'