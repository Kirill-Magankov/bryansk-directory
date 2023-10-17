from flask_restx import Resource, Namespace

from app.api.model.feedback import FeedbackModel
from app.api.model.schemas import FeedbackSchema

api = Namespace('Feedbacks')


@api.route('')
class FeedbackList(Resource):
    def get(self):
        feedbacks = FeedbackModel.query.all()
        return {'count': len(feedbacks),
                'data': FeedbackSchema(many=True).dump(feedbacks)}
