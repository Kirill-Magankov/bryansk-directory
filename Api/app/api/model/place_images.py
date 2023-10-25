from app.db import db
from app.utils.security_utils import get_uuid


class PlaceImageModel(db.Model):
    __tablename__ = 'place_images'

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    uuid = db.Column(db.String(36), nullable=False, default=get_uuid(), onupdate=get_uuid())
    image = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=False)
    url = db.Column(db.String(255))

    def __init__(self, image, uuid, url=None):
        self.image = image
        self.uuid = uuid
        self.url = url

    def __repr__(self): return '<Image Id %s>' % self.id
