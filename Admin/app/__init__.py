import os

from flask import Flask

from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

from app.routes import authorize, places, users, logout, place_type, neighborhoods,reviews,images
