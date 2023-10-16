from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from app.api.model.feedback import Feedback
from app.api.model.place import Place
from app.api.model.place_images import PlaceImage
from app.api.model.place_review import PlaceReview
from app.api.model.place_type import PlaceType
from app.api.model.user import User

from .marshmallow import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class PlaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Place

    place_type = ma.Nested('PlaceTypeSchema')
    place_reviews = ma.Nested('PlaceReviewSchema', many=True)


class PlaceTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceType


class PlaceImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceImage


class PlaceReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaceReview


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
