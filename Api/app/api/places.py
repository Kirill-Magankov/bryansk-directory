import io
from datetime import datetime

from flask import send_file, url_for
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage

from app.api.model.neighborhood import NeighborhoodModel
from app.api.model.nullable_string import NullableString
from app.api.model.place import PlaceModel
from app.api.model.place_images import PlaceImageModel
from app.api.model.place_review import PlaceReviewModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.schemas import PlaceSchema, NeighborhoodSchema, PlaceTypeSchema, PlaceReviewSchema, PlaceImageSchema
from app.db import db
from app.utils import messages
from app.utils.security_utils import get_uuid

api = Namespace('Places', 'Справочник доступных мест и информации связанной с ними')

# region Request place parser
place_parser = reqparse.RequestParser()
place_parser.add_argument('neighborhood', help='Фильтрация по району')
place_parser.add_argument('type', help='Тип места')
place_parser.add_argument('order', choices=['asc', 'desc'], default='desc')
# place_parser.add_argument('sort', help='Сортировка по параметру', default='grade')
# endregion

# region Swagger models
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, help='Изображение места',
                           required=True, location='files')

neighborhood_model = api.model('Neighborhood', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})

review_model = api.model('Review', {
    'id': fields.Integer(readonly=True),
    'date': fields.Date(default=datetime.now(), required=True),
    'author_name': NullableString,
    'description': NullableString,
    'url': NullableString,
    'grade': fields.Integer(required=True, default=5)
})

place_type_model = api.model('PlaceType`', {
    'id': fields.Integer(readonly=True),
    'type_name': fields.String(required=True),
    'description': NullableString()
})

place_model = api.model('Place', {
    'place_type': fields.Nested(place_type_model),
    'neighborhood': fields.Nested(neighborhood_model),
    'id': fields.Integer(readonly=True),
    'name': NullableString,
    'address': fields.String(required=True),
    'description': NullableString,
    'phone_number': NullableString,
    'grade': fields.Float,
})


# endregion


def get_model_data(model, payload, field_name):
    model_data = model.query
    model = model_data.filter(getattr(model, field_name) == payload.get(field_name)).first()

    # foreach for payloads keys and create the class with attributes?
    return model


# region Places
@api.route('')
class PlacesList(Resource):
    @api.expect(place_parser, validate=True)
    def get(self):
        """Список доступных мест"""
        parser_args = place_parser.parse_args()

        places = PlaceModel.query

        neighborhood = parser_args.get('neighborhood')
        place_type = parser_args.get('type')

        sort_by = parser_args.get('sort')
        place_order_by = parser_args.get('order')

        if neighborhood: places = places.join(NeighborhoodModel).filter(NeighborhoodModel.name == neighborhood)
        if place_type: places = places.join(PlaceTypeModel).filter(PlaceTypeModel.type_name == place_type)

        # # Sort and order
        # if sort_by and hasattr(PlaceModel, sort_by):
        #     if place_order_by == 'asc':
        #         places = places.order_by(getattr(PlaceModel, sort_by).asc())
        #     else:
        #         places = places.order_by(getattr(PlaceModel, sort_by).desc())

        places = places.order_by(PlaceModel.grade.asc()) \
            if place_order_by == 'asc' \
            else places.order_by(PlaceModel.grade.desc())

        places = places.all()
        if not places: return messages.ErrorMessage.entry_not_exist('Places')
        if len(places) == 0: return messages.InfoMessage.no_entry('places')

        return {'total': len(places),
                'data': PlaceSchema(many=True).dump(places)}

    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(place_model, validate=True)
    def post(self):
        """Добавление места"""
        data = api.payload

        try:
            if PlaceModel.query.filter(PlaceModel.name == data.get('name')).first():
                return {'message': 'The place is already exists'}, 400

            place_data = PlaceModel(
                name=data.get('name'),
                address=data.get('address'),
                description=data.get('description'),
                phone_number=data.get('phone_number'),
                grade=data.get('grade'),
            )

            place_type_payload = data.get('place_type')
            # noinspection PyTypeChecker
            place_type_data = get_model_data(PlaceTypeModel, place_type_payload, 'type_name')

            place_neighborhood_payload = data.get('neighborhood')
            # noinspection PyTypeChecker
            place_neighborhood_data = get_model_data(NeighborhoodModel, place_neighborhood_payload, 'name')

            if not place_type_data:
                place_type_data = PlaceTypeModel(type_name=place_type_payload.get('type_name'),
                                                 description=place_type_payload.get('description'))

            if not place_neighborhood_data:
                place_neighborhood_data = NeighborhoodModel(name=place_neighborhood_payload.get('name'))

            place_data.place_type = place_type_data
            place_data.neighborhood = place_neighborhood_data

            db.session.add(place_data)
            db.session.commit()

            return {'message': 'Place successfully added',
                    'data': PlaceSchema().dump(place_data)}
        except Exception as e:
            return messages.ErrorMessage.entry_not_exist(e)


@api.route('/<int:place_id>')
class PlaceById(Resource):
    def get(self, place_id):
        """Получение места по идентификатору"""
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')
        return {'data': PlaceSchema().dump(place)}

    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Обновление информации о месте"""
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        data = api.payload
        try:
            place.name = data.get('name')
            place.address = data.get('address')
            place.description = data.get('description')
            place.phone_number = data.get('phone_number')
            place.grade = data.get('grade')

            place_type_payload = data.get('place_type')
            # noinspection PyTypeChecker
            place_type_data = get_model_data(PlaceTypeModel, place_type_payload, 'type_name')

            place_neighborhood_payload = data.get('neighborhood')
            # noinspection PyTypeChecker
            place_neighborhood_data = get_model_data(NeighborhoodModel, place_neighborhood_payload, 'name')

            if not place_type_data:
                place_type_data = PlaceTypeModel(type_name=place_type_payload.get('type_name'),
                                                 description=place_type_payload.get('description'))

            if not place_neighborhood_data:
                place_neighborhood_data = NeighborhoodModel(name=place_neighborhood_payload.get('name'))

            place.place_type = place_type_data
            place.neighborhood = place_neighborhood_data

            db.session.commit()
            return {'message': 'Place successfully updated',
                    'data': PlaceSchema().dump(place)}

        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)

    @jwt_required()
    @api.doc(security='Bearer')
    def delete(self, place_id):
        """Удаление места"""
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        try:
            db.session.delete(place)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Place')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/<string:place_name>')
class PlaceByNameSearch(Resource):
    def get(self, place_name):
        """Поиск места по названию"""
        places = PlaceModel.query.filter(PlaceModel.name.like(f'%{place_name}%')).all()
        if not places or len(places) == 0: return messages.InfoMessage.no_entry('place')

        return {'total': len(places),
                'data': PlaceSchema(many=True).dump(places)}


# endregion

# region Types
@api.route('/types')
class PlacesTypeList(Resource):
    def get(self):
        """Получение категорий (типов) мест"""
        place_types = PlaceTypeModel.query.all()
        if not place_types: return messages.ErrorMessage.entry_not_exist('Place type')
        if len(place_types) == 0: return messages.InfoMessage.no_entry('place types')

        return {'total': len(place_types),
                'data': PlaceTypeSchema(many=True).dump(place_types)}

    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(place_type_model, validate=True)
    def post(self):
        """Добавление новой категории (типа) места"""
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
@api.doc(security='Bearer')
class PlaceTypeById(Resource):
    @jwt_required()
    def get(self, place_type_id):
        """Получение категории (типа) по идентификатору"""
        place_type = PlaceTypeModel.query.get(place_type_id)
        if not place_type: return messages.ErrorMessage.entry_not_exist('Place type')

        return {'data': PlaceTypeSchema().dump(place_type)}

    @jwt_required()
    @api.expect(place_type_model, validate=True)
    def put(self, place_type_id):
        """Обновление информации о категории (типа) места"""
        data = api.payload
        place_type_data = PlaceTypeModel.query.get(place_type_id)
        if not place_type_data: return messages.ErrorMessage.entry_not_exist('Place type')
        place_type_data.type_name = data.get('type_name', place_type_data.type_name)
        place_type_data.description = data.get('description', place_type_data.description)

        try:
            db.session.commit()
            return {'message': 'Place type successfully updated',
                    'data': PlaceTypeSchema().dump(place_type_data)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)

    @jwt_required()
    def delete(self, place_type_id):
        """Удаление категории (типа) места"""
        place_type = PlaceTypeModel.query.get(place_type_id)
        if not place_type: return messages.ErrorMessage.entry_not_exist('Place type')

        try:
            db.session.delete(place_type)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Place type')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


# endregion

# region Neighborhood
@api.route('/neighborhood')
class NeighborhoodsList(Resource):
    def get(self):
        """Получение доступных районов"""
        neighborhoods = NeighborhoodModel.query.all()
        if not neighborhoods: return messages.ErrorMessage.entry_not_exist('Neighborhood')
        if len(neighborhoods) == 0: return messages.InfoMessage.no_entry('neighborhoods')

        return {'total': len(neighborhoods),
                'data': NeighborhoodSchema(many=True).dump(neighborhoods)}

    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(neighborhood_model, validate=True)
    def post(self):
        """Добавление нового района"""
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
@api.doc(security='Bearer')
class NeighborhoodById(Resource):
    @jwt_required()
    def get(self, neighborhood_id):
        "Получение доступного района по идентификатору"
        neighborhood = NeighborhoodModel.query.get(neighborhood_id)
        if not neighborhood: return messages.ErrorMessage.entry_not_exist('Neighborhood')

        return {'data': NeighborhoodSchema().dump(neighborhood)}

    @jwt_required()
    @api.expect(neighborhood_model, validate=True)
    def put(self, neighborhood_id):
        """Обновление информации о районе"""
        data = api.payload
        neighborhood = NeighborhoodModel.query.get(neighborhood_id)
        if not neighborhood: return messages.ErrorMessage.entry_not_exist('Neighborhood')
        neighborhood.name = data.get('name', neighborhood.name)
        try:
            db.session.commit()
            return {'message': 'Neighborhood successfully updated',
                    'data': NeighborhoodSchema().dump(neighborhood)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)

    @jwt_required()
    def delete(self, neighborhood_id):
        """Удаление района"""
        neighborhood = NeighborhoodModel.query.get(neighborhood_id)
        if not neighborhood: return messages.ErrorMessage.entry_not_exist('Neighborhood')

        try:
            db.session.delete(neighborhood)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Neighborhood')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


# endregion

# region Images
@api.route('/<int:place_id>/images')
class PlaceImageByPlaceId(Resource):
    def get(self, place_id):
        """Получение доступных изображений для места"""
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')
        if len(place.images) == 0: return messages.InfoMessage.no_entry('images')
        return {'data': PlaceImageSchema(many=True).dump(place.images)}


@api.route('/images/<string:uuid>')
class PlaceImageByUuid(Resource):
    def get(self, uuid):
        """Получение изображения по его uuid"""
        place_image = PlaceImageModel.query.filter(PlaceImageModel.uuid == uuid).first()
        if not place_image: return messages.ErrorMessage.entry_not_exist('Image')
        return send_file(io.BytesIO(place_image.image), mimetype='image/jpeg')

    @jwt_required()
    @api.doc(security='Bearer')
    def delete(self, uuid):
        """Удаление изображения"""
        place_image = PlaceImageModel.query.filter(PlaceImageModel.uuid == uuid).first()
        if not place_image: return messages.ErrorMessage.entry_not_exist('Image')
        try:
            db.session.delete(place_image)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Image')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/<int:place_id>/uploadImage')
class PlaceUploadImage(Resource):
    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(upload_parser, validate=True)
    def post(self, place_id):
        """Добавление изображения для места"""
        parser_args = upload_parser.parse_args()
        file = parser_args.get('file')
        if not file: return messages.ErrorMessage.entry_not_exist('File')
        if not file.filename.lower().endswith(('.jpg', '.png')):
            return {'error': 'Unsupported file extension (available *.jpg, *.png)'}, 415

        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        place_image_model = PlaceImageModel(file.read(), get_uuid())
        place.images.append(place_image_model)

        try:
            db.session.commit()
            return {'message': 'Image successfully uploaded',
                    'data': 'Image uuid: %s' % place_image_model.uuid}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


# endregion

# region Review
@api.route('/<int:place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Получение доступных отзывов о месте"""
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')
        if len(place.reviews) == 0: return messages.InfoMessage.no_entry('reviews')
        return {'data': PlaceReviewSchema(many=True).dump(place.reviews)}

    @api.expect(review_model, validate=True)
    def post(self, place_id):
        """Добавление отзыва о месте"""
        data = api.payload
        place = PlaceModel.query.get(place_id)
        if not place: return messages.ErrorMessage.entry_not_exist('Place')

        review_data = PlaceReviewModel(date=datetime.strptime(data.get('date'), '%Y-%m-%d'),
                                       author_name=data.get('author_name'),
                                       description=data.get('description'),
                                       url=data.get('url'),
                                       grade=data.get('grade'))

        place.reviews.append(review_data)
        db.session.commit()
        return {'message': 'Place review successfully added',
                'data': PlaceReviewSchema().dump(review_data)}
        # try:
        #
        # except Exception as e:
        #     return messages.ErrorMessage.unexpected_error(e)


@api.route('/reviews/<int:review_id>')
@api.doc(security='Bearer')
class PlaceReviewById(Resource):
    @jwt_required()
    def delete(self, review_id):
        """Удаление отзыва по идентификатору места"""
        review_data = PlaceReviewModel.query.get(review_id)
        if not review_data: return messages.ErrorMessage.entry_not_exist('Place review')

        try:
            db.session.delete(review_data)
            db.session.commit()
            return messages.InfoMessage.entry_delete('Place review')
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)

# endregion
