from datetime import datetime

from app.db import db


class PlaceReviewModel(db.Model):
    __tablename__ = 'place_reviews'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.now(), onupdate=datetime.now())
    author_name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    url = db.Column(db.String(255))
    grade = db.Column(db.Integer, nullable=False)

    def __repr__(self): return '<Place Review %s>' % self.description
