from app.db import db


class Neighborhood(db.Model):
    __tablename__ = 'neighborhood'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    places = db.relationship('place', backref='neighborhood', lazy=True)

    def __repr__(self): return '<Neighborhood %s>' % self.neighborhood
