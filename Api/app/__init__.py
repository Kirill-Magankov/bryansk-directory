import threading
import time
from urllib import request
from urllib.error import HTTPError

from flask import Flask, redirect
from flask_cors import CORS
from healthcheck import HealthCheck
from sqlalchemy import text

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

    with app.app_context(): app.register_blueprint(create_api(), url_prefix=app.config.get('API_URL'))

    from .api.bcrypt import bcrypt
    bcrypt.init_app(app)

    return app


def mysql_available():
    from .db import db
    try:
        db.session.execute(text('SELECT 1'))
        return True, 'mysql ok'
    except Exception as e:
        return False, 'error: %s' % e


app = create_app()

health = HealthCheck()
health.add_check(mysql_available)
app.add_url_rule(f'{app.config.get("API_URL")}/health', 'health', view_func=lambda: health.run())


@app.route('/')
def index(): return redirect(app.config.get('API_URL'))


class DataModelList:
    class DataModel:
        def __init__(self, id_, user_id, message, status='Open', comment=None):
            self.id = id_
            self.user_id = user_id
            self.message = message
            self.status = status
            self.comment = comment

    datas = [
        DataModel(1, 8, 'The feedback text # 1'),
        DataModel(2, 12, 'The feedback text # 2'),
        DataModel(3, 12, 'The feedback text # 3'),
        DataModel(4, 13, 'The feedback text # 4'),
    ]

    def get(self, id_):
        if data := [i for i in self.datas if i.id == id_]:
            if len(data) >= 0: return data[0]
        return None


TIMEOUT = 30

data_list = DataModelList()


@app.route('/feedback-notify/<int:id_>')
def poll(id_):
    start = time.time()
    while time.time() - start < TIMEOUT:
        entry = data_list.get(id_)
        if not entry: return {'message': 'No available data'}, 400

        if entry.status == 'closed':
            return {'message': 'Feedback No. %i closed.' % entry.id,
                    'events': {
                        'type': 'feedback_close',
                        'data': {
                            'user_id': entry.user_id,
                            'comment': entry.comment
                        }
                    }}
        time.sleep(2)

    return {'events': []}, 200


@app.route('/closeFeedback/<int:id_>')
def close_feedback(id_):
    entry = data_list.get(id_)
    if not entry: return {'message': 'No data to display'}
    if entry.status == 'closed': return {'message': 'Feedback already closed.'}
    entry.status = 'closed'
    print(entry.__dict__)
    return {'message': 'Feedback No. %i closed.' % entry.id}


@app.route('/openFeedback/<int:id_>')
def open_feedback(id_):
    entry = data_list.get(id_)
    if not entry: return {'message': 'No data to display'}
    if entry.status == 'open': return {'message': 'Feedback already open.'}
    entry.status = 'open'
    print(entry.__dict__)
    return {'message': 'Feedback No. %i open.' % entry.id}


@app.route('/client')
def client_test():
    try:
        response = request.urlopen('http://localhost:8000/feedback-notify/1', timeout=TIMEOUT)
        return response
    except TimeoutError:
        client_test()
