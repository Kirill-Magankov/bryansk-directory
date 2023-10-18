from app.db import db
from .place import PlaceModel


class NeighborhoodModel(db.Model):
    __tablename__ = 'neighborhood'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    places = db.relationship('PlaceModel', backref='neighborhood', lazy=True, passive_deletes=True)

    def __init__(self, name): self.name = name

    def __repr__(self): return '<Neighborhood %s>' % self.name
