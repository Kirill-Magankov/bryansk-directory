import io
from datetime import datetime

from flask import send_file, url_for
from flask_restx import Namespace, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage

from app.api.model.neighborhood import NeighborhoodModel
from app.api.model.place import PlaceModel
from app.api.model.place_images import PlaceImageModel
from app.api.model.place_review import PlaceReviewModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.schemas import PlaceSchema, NeighborhoodSchema, PlaceTypeSchema, PlaceReviewSchema, PlaceImageSchema
from app.db import db
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


@api.route('/<int:place_id>')
class PlaceById(Resource):
    def get(self, place_id):
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        return {'data': PlaceSchema().dump(place)}


review_model = api.model('Review', {
    'id': fields.Integer(readonly=True),
    'date': fields.DateTime(default=datetime.now(), required=True),
    'author_name': fields.String(),
    'description': fields.String(),
    'url': fields.String(),
    'grade': fields.Integer(required=True, default=5)
})


@api.route('/<int:place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')
        return {'data': PlaceReviewSchema(many=True).dump(place.reviews)}

    @api.expect(review_model, validate=True)
    def post(self, place_id):
        data = api.payload
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        review_data = PlaceReviewModel(date=data.get('date'),
                                       author_name=data.get('author_name'),
                                       description=data.get('description'),
                                       url=data.get('url'),
                                       grade=data.get('grade'))

        try:
            place.reviews.append(review_data)
            db.session.commit()
            return {'message': 'Place review successfully added',
                    'data': PlaceReviewSchema().dump(review_data)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/reviews/<int:review_id>')
class PlaceReviewById(Resource):
    def delete(self, review_id):
        review_data = PlaceReviewModel.query.get(review_id)
        if not review_data: return messages.ErrorMessage.entry_not_exist('Place review')

        try:
            db.session.delete(review_data)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Place review')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/<int:place_id>/images')
class PlaceImageById(Resource):
    def get(self, place_id):
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')
        return {'data': PlaceImageSchema(many=True).dump(place.images)}


upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, help='Изображение места',
                           required=True, location='files')


@api.route('/<int:place_id>/uploadImage')
class PlaceUploadImage(Resource):
    @api.expect(upload_parser)
    def post(self, place_id):
        parser_args = upload_parser.parse_args()
        file = parser_args.get('file')
        if not file: return messages.ErrorMessage.entry_not_exist('File')
        if not file.filename.lower().endswith(('.jpg', '.png')):
            return {'error': 'Unsupported file extension (available *.jpg, *.png)'}, 415

        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        place_image_model = PlaceImageModel(file.read())
        place.images.append(place_image_model)

        try:
            db.session.commit()
            return {'message': 'Image uploaded successfully',
                    'data': 'Image uuid: %s' % place_image_model.uuid}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


neighborhood_model = api.model('Neighborhood', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})


@api.route('/neighborhood')
class NeighborhoodsList(Resource):
    def get(self):
        neighborhoods = NeighborhoodModel.query.all()
        if not neighborhoods: return messages.ErrorMessage.entry_not_exist('Neighborhood')
        return {'count': len(neighborhoods),
                'data': NeighborhoodSchema(many=True).dump(neighborhoods)}

    @api.expect(neighborhood_model, validate=True)
    def post(self):
        data = api.payload
        neighborhood = NeighborhoodModel(name=data.get('name', 'undefined'))

        try:
            db.session.add(neighborhood)
            db.session.commit()
            return {'message': 'Neighborhood successfully added',
                    'data': NeighborhoodSchema().dump(neighborhood)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/neighborhood/<int:neighborhood_id>')
class NeighborhoodById(Resource):
    def delete(self, neighborhood_id):
        neighborhood = NeighborhoodModel.query.get(neighborhood_id)
        if not neighborhood: return messages.ErrorMessage.entry_not_exist('Neighborhood')

        try:
            db.session.delete(neighborhood)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Neighborhood')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


place_type_model = api.model('Place', {
    'id': fields.Integer(readonly=True),
    'type_name': fields.String(required=True),
    'description': fields.String()
})


@api.route('/types')
class PlacesTypeList(Resource):
    def get(self):
        place_types = PlaceTypeModel.query.all()
        if not place_types: return messages.ErrorMessage.entry_not_exist('Place type')
        return {'count': len(place_types),
                'data': PlaceTypeSchema(many=True).dump(place_types)}

    @api.expect(place_type_model, validate=True)
    def post(self):
        data = api.payload
        place_type = PlaceTypeModel(type_name=data.get('type_name'),
                                    description=data.get('description'))

        try:
            db.session.add(place_type)
            db.session.commit()
            return {'message': 'Place type successfully added',
                    'data': PlaceTypeSchema().dump(place_type)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/types/<int:place_type_id>')
class PlaceTypeById(Resource):
    def delete(self, place_type_id):
        place_type = PlaceTypeModel.query.get(place_type_id)
        if not place_type: return messages.ErrorMessage.entry_not_exist('Place type')

        try:
            db.session.delete(place_type)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Place type')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/images/<string:uuid>')
class PlaceImageByUuid(Resource):
    def get(self, uuid):
        place_image = PlaceImageModel.query.filter(PlaceImageModel.uuid == uuid).first()
        if not place_image: return messages.ErrorMessage.entry_not_exist('Image')
        return send_file(io.BytesIO(place_image.image), mimetype='image/jpeg')

    def delete(self, uuid):
        place_image = PlaceImageModel.query.filter(PlaceImageModel.uuid == uuid).first()
        if not place_image: return messages.ErrorMessage.entry_not_exist('Image')
        try:
            db.session.delete(place_image)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Image')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)
