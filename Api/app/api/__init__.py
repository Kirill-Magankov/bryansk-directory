from flask import Blueprint, current_app
from flask_jwt_extended import JWTManager
from flask_restx import Api

from .users import api as users
from .places import api as places
from .feedback import api as feedback
from ..utils.blocklist import BLOCKLIST

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload): return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"message": "The token has been revoked.", "error": "token_revoked"}, 401


authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter the token with the `Bearer` prefix'
    }
}


def create_api():
    blueprint = Blueprint('api', __name__)

    api = Api(blueprint, title=current_app.config.get('API_TITLE'),
              version=current_app.config.get('API_VERSION'),
              authorizations=authorizations,
              description=current_app.config.get('API_DESCRIPTION'))

    api.add_namespace(users, '/users')
    api.add_namespace(places, '/places')
    api.add_namespace(feedback, '/feedbacks')

    return blueprint
