import requests
from flask import request, redirect, url_for, render_template

from app import app
from app.constant import menu


@app.route('/images/<place_id>')
def image_list(place_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/" + place_id + "/images"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.get(api_url, headers=headers)
    images_uuid_list = []
    for item in response.json()['data']:
        images_uuid_list.append(item['uuid'])

    return render_template('images.html', menu=menu, title='Изображения места', user_list=response.json()['data'])
