from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace, fields, reqparse

from app.api.model.feedback import FeedbackModel
from app.api.model.nullable_string import NullableString
from app.api.model.schemas import FeedbackSchema
from app.db import db
from app.utils import messages

api = Namespace('Feedbacks', 'Обратная связь')

feedback_model = api.model('Feedback', {
    'id': fields.Integer(readonly=True),
    'tg_username': NullableString,
    'tg_user_id': fields.String(required=True),
    'tg_chat_id': fields.String(required=True),
    'email': NullableString,
    'status': fields.String(readonly=True),
    'message': NullableString,
    'comment': fields.String(readonly=True),
})
feedback_model_put = api.model('FeedbackStatus', {
    'id': fields.Integer(readonly=True),
    'status': fields.String(required=True, enum=['Closed', 'Open']),
    'comment': NullableString,
})

feedback_parser = reqparse.RequestParser()
feedback_parser.add_argument('status', choices=['Open', 'Closed'])


@api.route('')
class FeedbackList(Resource):
    @jwt_required()
    @api.doc(security='Bearer')
    @api.expect(feedback_parser)
    def get(self):
        """Получение списка заявок"""
        status = feedback_parser.parse_args().get('status')
        feedbacks = FeedbackModel.query

        if status: feedbacks = feedbacks.filter(FeedbackModel.status == status)
        feedbacks = feedbacks.all()
        if not feedbacks: return messages.ErrorMessage.entry_not_exist('Feedbacks')
        if len(feedbacks) == 0: return messages.InfoMessage.no_entry('feedbacks')
        return {'total': len(feedbacks),
                'data': FeedbackSchema(many=True).dump(feedbacks)}

    @api.expect(feedback_model, validate=True)
    def post(self):
        """Добавление заявки (обратной связи)"""
        data = api.payload

        feedback = FeedbackModel(tg_username=data.get('tg_username'), tg_user_id=data.get('tg_user_id'),
                                 tg_chat_id=data.get('tg_chat_id'), email=data.get('email'),
                                 message=data.get('message'))
        try:
            db.session.add(feedback)
            db.session.commit()
            return {'message': 'Feedback successfully added',
                    'data': FeedbackSchema().dump(feedback)}

        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)


@api.route('/<int:feedback_id>')
@api.doc(security='Bearer')
class FeedbackById(Resource):
    @jwt_required()
    def get(self, feedback_id):
        """Получение заявки по идентификатору"""
        feedback = FeedbackModel.query.get(feedback_id)
        if not feedback: return messages.ErrorMessage.entry_not_exist('Feedback')
        return {'data': FeedbackSchema().dump(feedback)}

    @jwt_required()
    @api.expect(feedback_model_put, validate=True)
    def put(self, feedback_id):
        """Обновление статуса заявки"""
        feedback = FeedbackModel.query.get(feedback_id)
        if not feedback: return messages.ErrorMessage.entry_not_exist('Feedback')

        data = api.payload
        if feedback.status == 'Closed': return {'message': 'Feedback already closed'}
        if data.get('status') == 'Open': return {'message': 'Feedback already open'}

        try:
            feedback: FeedbackModel
            feedback.status = data.get('status')
            feedback.comment = data.get('comment')
            db.session.commit()
            return {'message': 'Feedback status successfully updated',
                    'data': FeedbackSchema().dump(feedback)}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)

    @jwt_required()
    def delete(self, feedback_id):
        """Удаление заявки"""
        feedback = FeedbackModel.query.get(feedback_id)
        if not feedback: return messages.ErrorMessage.entry_not_exist('Feedback')

        try:
            db.session.delete(feedback)
            db.session.commit()
            return {'message': 'Feedback successfully deleted'}
        except Exception as e:
            return messages.ErrorMessage.unexpected_error(e)
