import os

import requests
from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from app import app
from app.constant import menu, api_url
from app.forms.images import imageForm


@app.route('/images/<place_id>')
def image_list(place_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))

    image_url = api_url + "places/images/"
    headers = {'Authorization': 'Bearer %s' % acces_token}

    try:
        response = requests.get(api_url + "places/" + place_id + "/images", headers=headers).json()['data']
    except KeyError:
        response = {}
    images_list = []
    for item in response:
        images_list.append(item['uuid'])
    return render_template('images.html', menu=menu, title='Изображения места', image_url=image_url, place_id=place_id,
                           images=images_list)


@app.route('/image_add/<place_id>', methods=["GET", "POST"])
def image_add(place_id):
    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % access_token}
    form = imageForm(request.files, crfs=True)
    if request.method == "POST":
        if 'image' not in request.files:
            flash('Не указан путь к файлу', 'danger')
            return redirect(request.url)
        file = form.image.data
        if file.filename == '':
            flash('Файл не выбран', 'danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            files = {'file': (filename, file, 'multipart/form-data')}
            response = requests.post(api_url + "places/"+place_id+"/uploadImage", headers=headers, files=files)
            if response.status_code == 200:
                return redirect(url_for('image_list', place_id=place_id))
            else:
                flash("Не удалось загрузить изображение", "danger")
    return render_template('imageForm.html', menu=menu, title='Добавление картинки', form=form)


@app.route('/image_delete/<uuid>', methods=["GET", "DELETE"])
def delete_image(uuid):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + 'places/images/' + uuid, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('places_list'))
