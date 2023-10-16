from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from config import Config

from app.api.model import place, place_type, place_images, user, neighborhood, place_review, feedback


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    from .db import db, migrations
    db.init_app(app)
    migrations.init_app(app, db)

    from .api.model.marshmallow import ma
    ma.init_app(app)

    from .api import blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app


app = create_app()
bcrypt = Bcrypt(app)
