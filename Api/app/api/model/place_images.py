from app.db import db


class PlaceImage(db.Model):
    __tablename__ = 'place_images'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)

    def __repr__(self): return '<Image Id %s>' % self.id
