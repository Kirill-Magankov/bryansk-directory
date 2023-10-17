from datetime import timedelta

from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from flask_restx import Namespace, Resource, fields

from app.api.model.schemas import UserSchema
from app.api.model.user import UserModel
from app.utils import messages
from app.utils.blocklist import BLOCKLIST
from app.utils.security_utils import password_hash_compare

api = Namespace('Users')

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

login_fields = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'remember': fields.Boolean(default=False)
})


@api.route('/login')
class UserLoginResource(Resource):
    @api.expect(login_fields, validate=True)
    def post(self):
        """Login user into the system"""
        data = api.payload
        user = UserModel.query.filter(UserModel.username == data.get('username')).first()

        if user:
            if password_hash_compare(user.password, data.get('password')):
                expires_delta = timedelta(days=15) if data.get('remember') else None

                access_token = create_access_token(identity=user.id, fresh=True,
                                                   expires_delta=expires_delta)
                return {
                    'message': 'User login successful',
                    'access_token': access_token
                }
            else:
                return messages.ErrorMessage.login_or_pass_error()
        else:
            return messages.ErrorMessage.user_not_exist()


@api.route('/logout')
class UserLogout(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Logout user from system"""
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return messages.InfoMessage.user_logout()


@api.route('/')
class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        return {'count': len(users),
                'data': UserSchema(many=True).dump(users)}
