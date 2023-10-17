from app.db import db


class FeedbackModel(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    tg_username = db.Column(db.String(255))
    tg_user_id = db.Column(db.Integer, nullable=False)
    tg_chat_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255))
    message = db.Column(db.String(255))

    def __repr__(self):
        return '<Feedback user_id: %s, chat_id: %s (%s)>' % self.tg_user_id, self.tg_chat_id, self.message
