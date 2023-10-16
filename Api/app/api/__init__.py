from flask import Blueprint
from flask_restx import Api, Resource

from .places import api as places

blueprint = Blueprint('api', __name__)

api = Api(blueprint, title='Справочник города Брянска',
          version='0.1', description='API документация для проекта "Справочник города Брянска"')

api.add_namespace(places, '/places')
