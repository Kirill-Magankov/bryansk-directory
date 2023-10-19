from datetime import timedelta

from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from flask_restx import Namespace, Resource, fields

from app.api.model.schemas import UserSchema
from app.api.model.user import UserModel
from app.db import db
from app.utils import messages
from app.utils.blocklist import BLOCKLIST
from app.utils.security_utils import password_hash_compare, password_hash_generate

api = Namespace('Users', 'Пользователи системы')

# region Swagger model schema
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


# endregion

@api.route('')
@api.doc(security='Bearer')
class Users(Resource):
    @jwt_required()
    def get(self):
        """Получение доступных пользователей"""
        users = UserModel.query.all()
        if not users: return messages.ErrorMessage.entry_not_exist('User')
        return {'total': len(users),
                'data': UserSchema(many=True).dump(users)}

    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):
        """Добавление пользователя"""
        data = api.payload

        try:
            password = password_hash_generate(data.get('password'))
            user = UserModel(data.get('username'), password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'User successfully added',
                    'data': UserSchema().dump(user)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/<int:user_id>')
@api.doc(security='Bearer')
class UserById(Resource):
    @jwt_required()
    def get(self, user_id):
        """Получение пользователя по идентификатору"""
        user = UserModel.query.get(user_id)
        if not user: return messages.ErrorMessage.user_not_exist()

        return {'data': UserSchema().dump(user)}

    @jwt_required()
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """Обновление информации о пользователе"""
        user = UserModel.query.get(user_id)
        if not user: return messages.ErrorMessage.user_not_exist()

        data = api.payload
        user.username = data.get('username')
        user.password = password_hash_generate(data.get('password'))
        try:
            db.session.commit()
            return {'message': 'User successfully updated',
                    'data': UserSchema().dump(user)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/login')
class UserLoginResource(Resource):
    @api.expect(login_fields, validate=True)
    def post(self):
        """Авторизация пользователя в системе"""
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
        """Выход пользователя из системы"""
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return messages.InfoMessage.user_logout()
