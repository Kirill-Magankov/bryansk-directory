from flask_restx import Resource, Namespace

from app.api.model.feedback import FeedbackModel
from app.api.model.schemas import FeedbackSchema
from app.utils import messages

api = Namespace('Feedbacks', 'Обратная связь')


@api.deprecated
@api.route('')
class FeedbackList(Resource):
    def get(self):
        """Получение списка заявок"""
        feedbacks = FeedbackModel.query.all()
        if not feedbacks: return messages.ErrorMessage.entry_not_exist('Feedbacks')
        return {'total': len(feedbacks),
                'data': FeedbackSchema(many=True).dump(feedbacks)}
