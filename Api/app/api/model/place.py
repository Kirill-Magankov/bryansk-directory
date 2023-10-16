from app.db import db
from .place_images import PlaceImage
from .place_review import PlaceReview


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(255))
    phone_number = db.Column(db.String(11))
    grade = db.Column(db.Float)

    images = db.relationship('PlaceImage', backref='place', lazy=True, passive_deletes=True)
    place_reviews = db.relationship('PlaceReview', backref='place', lazy=True, passive_deletes=True)

    def __repr__(self): return "<Place %s>" % self.name
