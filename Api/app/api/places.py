from flask_restx import Namespace, Resource

api = Namespace('Places')


@api.route('/')
class Places(Resource):
    def get(self):
        return {}
