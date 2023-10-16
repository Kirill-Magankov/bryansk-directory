from app.db import db
from .place import Place


class Neighborhood(db.Model):
    __tablename__ = 'neighborhood'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    places = db.relationship('Place', backref='neighborhood', lazy=True, passive_deletes=True)

    def __repr__(self): return '<Neighborhood %s>' % self.neighborhood
