from app.db import db


class PlaceReview(db.Model):
    __tablename__ = 'place_reviews'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))

    def __repr__(self): return '<Place Review %s>' % self.description
