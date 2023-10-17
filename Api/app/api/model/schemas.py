from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from app.api.model.feedback import FeedbackModel
from app.api.model.place import PlaceModel
from app.api.model.place_images import PlaceImageModel
from app.api.model.place_review import PlaceReviewModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.user import UserModel

from .marshmallow import ma
from .neighborhood import NeighborhoodModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel


class PlaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceModel

    place_type = ma.Nested('PlaceTypeSchema')
    place_reviews = ma.Nested('PlaceReviewSchema', many=True)
    images = ma.Nested('PlaceImageSchema', many=True)


class NeighborhoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NeighborhoodModel


class PlaceTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceTypeModel


class PlaceImageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uuid')


class PlaceReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceReviewModel


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FeedbackModel
