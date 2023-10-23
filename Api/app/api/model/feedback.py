from app.db import db


class FeedbackModel(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    tg_username = db.Column(db.String(255))
    tg_user_id = db.Column(db.String(15), nullable=False)
    tg_chat_id = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255))
    status = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(255))

    def __init__(self, tg_user_id, tg_chat_id, status='Open', tg_username=None, email=None, message=None, comment=None):
        self.tg_username = tg_username
        self.tg_user_id = tg_user_id
        self.tg_chat_id = tg_chat_id
        self.email = email
        self.status = status
        self.message = message
        self.comment = comment

    def __repr__(self):
        return '<Feedback user_id: %s, chat_id: %s (%s)>' % self.tg_user_id, self.tg_chat_id, self.message
