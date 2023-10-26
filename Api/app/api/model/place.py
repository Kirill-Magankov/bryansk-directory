from app.db import db
from .place_images import PlaceImageModel
from .place_review import PlaceReviewModel


class PlaceModel(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(255))
    phone_number = db.Column(db.String(11))
    grade = db.Column(db.Float, nullable=False, default=0)

    images = db.relationship('PlaceImageModel', backref='place', lazy=True, passive_deletes=True)
    reviews = db.relationship('PlaceReviewModel', backref='place', lazy=True, passive_deletes=True)

    def __init__(self, name, address, description=None, phone_number=None, grade=0):
        self.name = name
        self.address = address
        self.description = description
        self.phone_number = phone_number
        self.grade = grade

    def __repr__(self): return "<Place %s>" % self.name
