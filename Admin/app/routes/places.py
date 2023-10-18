from flask import render_template

from app import app
from app.constant import menu


@app.route('/places')
def places_list():
    return render_template('places.html', menu=menu, title='Список мест')
