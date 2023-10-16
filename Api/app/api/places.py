from flask_restx import Namespace, Resource

from app.api.model.place import Place
from app.api.model.schemas import PlaceSchema

api = Namespace('Places')


@api.route('/')
class Places(Resource):
    def get(self):
        places = Place.query.all()
        return {'count': len(places),
                'data': PlaceSchema(many=True).dump(places)}
