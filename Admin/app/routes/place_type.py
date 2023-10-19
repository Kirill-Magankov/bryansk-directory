import requests
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.constant import menu
from app.forms.place_type import typeForm



@app.route('/place_types')
def place_types_list():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/types"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    try:
        response = requests.get(api_url, headers=headers).json()['data']
    except KeyError:
        response = {}
    return render_template('placeTypes.html', menu=menu, title='Список типов мест',
                           type_list=response)


@app.route('/place_type_add', methods=["GET", "POST"])
def place_type_add():
    form = typeForm(request.form, crsf=True)
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    if form.validate_on_submit():
        type_name = form.type_name.data
        description = form.description.data
        api_url = "http://localhost:8000/api/v1/places/types"
        data = {
            "type_name": type_name,
            "description": description
        }
        headers = {'Authorization': 'Bearer %s' % acces_token}
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.place_types_list'))
        else:
            flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('typeForm.html', menu=menu, title='Добавление типа места', form=form)


@app.route('/place_type_edit/<place_type_id>', methods=["GET", "POST"])
def edit_type(place_type_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/types/"

    headers = {'Authorization': 'Bearer %s' % acces_token}
    form = typeForm(request.form, crsf=True)
    if request.method == "GET":
        cur_name = requests.get(api_url + place_type_id, headers=headers)
        form.type_name.data = cur_name.json()['data'].get('type_name')
        form.description.data = cur_name.json()['data'].get('description')

    if request.method == "POST" and form.validate_on_submit():

        type_name = form.type_name.data
        description = form.description.data

        data = {
            "type_name": type_name,
            "description": description
        }

        response = requests.put(api_url + place_type_id, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.place_types_list'))
        else:
            flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('typeForm.html', menu=menu, title='Редактирование типа места', form=form)


@app.route('/place_type_delete/<place_type_id>', methods=["GET", "DELETE"])
def delete_type(place_type_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/types/"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + place_type_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('.place_types_list'))
