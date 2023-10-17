from flask_restx import Namespace, Resource

from app.api.model.neighborhood import NeighborhoodModel
from app.api.model.place import PlaceModel
from app.api.model.place_images import PlaceImageModel
from app.api.model.place_review import PlaceReviewModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.schemas import PlaceSchema, NeighborhoodSchema, PlaceTypeSchema, PlaceReviewSchema

api = Namespace('Places')


@api.route('')
class PlacesList(Resource):
    def get(self):
        places = PlaceModel.query.all()
        return {'count': len(places),
                'data': PlaceSchema(many=True).dump(places)}


@api.route('/neighborhood')
class NeighborhoodsList(Resource):
    def get(self):
        neighborhoods = NeighborhoodModel.query.all()
        return {'count': len(neighborhoods),
                'data': NeighborhoodSchema(many=True).dump(neighborhoods)}


@api.route('/types')
class PlacesTypeList(Resource):
    def get(self):
        place_types = PlaceTypeModel.query.all()
        return {'count': len(place_types),
                'data': PlaceTypeSchema(many=True).dump(place_types)}


@api.route('/reviews')
class PlaceReviewsList(Resource):
    def get(self):
        place_review = PlaceReviewModel.query.all()
        return {'count': len(place_review),
                'data': PlaceReviewSchema(many=True).dump(place_review)}


@api.route('/images')
class PlaceImagesList(Resource):
    def get(self):
        images = PlaceImageModel.query.all()
        return {'count': len(images)}
