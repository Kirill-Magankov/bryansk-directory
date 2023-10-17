import io

from flask import send_file, url_for
from flask_restx import Namespace, Resource, reqparse
from sqlalchemy import desc

from app.api.model.neighborhood import NeighborhoodModel
from app.api.model.place import PlaceModel
from app.api.model.place_images import PlaceImageModel
from app.api.model.place_review import PlaceReviewModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.schemas import PlaceSchema, NeighborhoodSchema, PlaceTypeSchema, PlaceReviewSchema, PlaceImageSchema
from app.utils import messages

api = Namespace('Places')

place_parser = reqparse.RequestParser()
place_parser.add_argument('neighborhood', help='Фильтрация по району')
place_parser.add_argument('type', help='Тип места')
place_parser.add_argument('sort', help='Сортировка по параметру', default='grade')
place_parser.add_argument('order', choices=['asc', 'desc'], default='desc')


@api.route('')
class PlacesList(Resource):
    @api.expect(place_parser)
    def get(self):
        parser_args = place_parser.parse_args()

        places = PlaceModel.query

        neighborhood = parser_args.get('neighborhood')
        place_type = parser_args.get('type')

        sort_by = parser_args.get('sort')
        place_order_by = parser_args.get('order')

        if neighborhood: places = places.join(NeighborhoodModel).filter(NeighborhoodModel.name == neighborhood)
        if place_type: places = places.join(PlaceTypeModel).filter(PlaceTypeModel.type_name == place_type)

        if sort_by and hasattr(PlaceModel, sort_by):
            if place_order_by == 'asc':
                places = places.order_by(getattr(PlaceModel, sort_by).asc())
            else:
                places = places.order_by(getattr(PlaceModel, sort_by).desc())

        places = places.all()
        if not places: return messages.ErrorMessage.entry_not_exist('Place')
        return {'count': len(places),
                'data': PlaceSchema(many=True).dump(places)}


@api.route('/neighborhood')
class NeighborhoodsList(Resource):
    def get(self):
        neighborhoods = NeighborhoodModel.query.all()
        if not neighborhoods: return messages.ErrorMessage.entry_not_exist('Neighborhood')
        return {'count': len(neighborhoods),
                'data': NeighborhoodSchema(many=True).dump(neighborhoods)}


@api.route('/types')
class PlacesTypeList(Resource):
    def get(self):
        place_types = PlaceTypeModel.query.all()
        if not place_types: return messages.ErrorMessage.entry_not_exist('Place type')
        return {'count': len(place_types),
                'data': PlaceTypeSchema(many=True).dump(place_types)}


@api.route('/reviews')
class PlaceReviewsList(Resource):
    def get(self):
        place_review = PlaceReviewModel.query.all()
        if not place_review: return messages.ErrorMessage.entry_not_exist('Place review')
        return {'count': len(place_review),
                'data': PlaceReviewSchema(many=True).dump(place_review)}


@api.route('/images/<string:uuid>')
class PlaceImage(Resource):
    def get(self, uuid):
        place_image = PlaceImageModel.query.filter(PlaceImageModel.uuid == uuid).first()
        if not place_image: return messages.ErrorMessage.entry_not_exist('Image')
        return send_file(io.BytesIO(place_image.image), mimetype='image/jpeg')
