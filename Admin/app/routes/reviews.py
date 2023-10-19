import requests
from flask import render_template, request, redirect, url_for

from app import app
from app.constant import menu


@app.route('/reviews/<place_id>')
def reviews_list(place_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/" + place_id + "/reviews"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    try:
        response = requests.get(api_url, headers=headers).json()['data']
    except KeyError:
        response = {}
    return render_template('reviews.html', menu=menu, title='Список отзывов о месте',
                           reviews_list=response)


@app.route('/reviews/<place_id>/review_id')
def delete_reviews(place_id, review_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/" + place_id + "/reviews/" + review_id
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('places_list'))
