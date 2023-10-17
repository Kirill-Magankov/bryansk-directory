from app.db import db
from .place import PlaceModel


class PlaceTypeModel(db.Model):
    __tablename__ = 'place_type'

    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    places = db.relationship('PlaceModel', backref='place_type', lazy=True, passive_deletes=True)

    def __repr__(self): return '<Place type %s>' % self.type_name
