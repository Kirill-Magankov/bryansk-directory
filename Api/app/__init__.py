from flask import Flask, redirect
from flask_cors import CORS

from app.utils.blocklist import BLOCKLIST
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

    from .api import jwt, create_api
    jwt.init_app(app)

    with app.app_context(): app.register_blueprint(create_api(), url_prefix='/api/v1')

    from .api.bcrypt import bcrypt
    bcrypt.init_app(app)

    return app


app = create_app()


@app.route('/')
def index(): return redirect('/api/v1')
