from app.db import db


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id'), nullable=False)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255), nullable=False)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    grade = db.Column(db.Float)

    images = db.relationship('place_images', backref='place', lazy=True)
    place_reviews = db.relationship('place_reviews', backref='place', lazy=True)

    def __repr__(self): return "<Place %s>" % self.name
