from flask_restx import Namespace, Resource

from app.api.model.schemas import UserSchema
from app.api.model.user import User

api = Namespace('Users')


@api.route('/')
class Users(Resource):
    def get(self):
        users = User.query.all()
        return {'count': len(users),
                'data': UserSchema(many=True).dump(users)}
