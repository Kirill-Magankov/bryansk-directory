from urllib.parse import urlencode

import requests
from flask import render_template, request, redirect, url_for
from flask_paginate import get_page_parameter, Pagination

from app import app
from app.constant import menu
from app.forms.places import placeForm, filterForm


def paginate_data(data, page, per_page):
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = -(-total // per_page)  # округление вверх
    return data[start:end], total_pages


@app.route('/places', methods=["GET", "POST"])
def places_list():
    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    api_url = "http://localhost:8000/api/v1/places"
    headers = {'Authorization': f'Bearer {access_token}'}
    filter_url = "http://localhost:8000/api/v1/places/types"
    neigh_url = "http://localhost:8000/api/v1/places/neighborhood"

    neighborhoods = requests.get(neigh_url, headers=headers)
    types = requests.get(filter_url, headers=headers)

    try:
        res_neighs = neighborhoods.json()['data']
        res_types = types.json()['data']
    except KeyError:
        res_neighs = []
        res_types = []

    names_neighs = [item['name'] for item in res_neighs]
    names_types = [item['type_name'] for item in res_types]

    form = filterForm(request.form, crsf=True)

    form.neighborhood.choices = [('', 'По району')] + [(item, item) for item in names_neighs]
    form.place_type.choices = [('', 'По типу места')] + [(item, item) for item in names_types]

    page = request.args.get('page', 1, type=int)
    per_page = 5

    if request.method == "GET":
        response = requests.get(api_url, headers=headers)
        try:
            places_data = response.json()['data']
        except KeyError:
            places_data = []
        paginated_data, total_pages = paginate_data(places_data, page, per_page)

        pagination = Pagination(page=page, total=total_pages, per_page=per_page, record_name='places_data',
                                css_framework='bootstrap4')

        return render_template('places.html', menu=menu, title='Список мест', places_list=paginated_data, form=form,
                               pagination=pagination)

    elif request.method == "POST":
        params = {}

        if form.place_type.data:
            params['type'] = form.place_type.data

        if form.neighborhood.data:
            params['neighborhood'] = form.neighborhood.data

        if form.sort.data:
            params['sort'] = form.sort.data

        response = requests.get(api_url, headers=headers, params=params)
        try:
            places_data = response.json()['data']
        except KeyError:
            places_data = []

        return render_template('places.html', menu=menu, title='Список мест', places_list=places_data, form=form)


@app.route('/place_add', methods=["GET", "POST"])
def place_add():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    form = placeForm(request.form, crsf=True)
    headers = {'Authorization': 'Bearer %s' % acces_token}
    neigh_url = "http://localhost:8000/api/v1/places/neighborhood"
    types_url = "http://localhost:8000/api/v1/places/types"
    neighborhoods = requests.get(neigh_url, headers=headers)
    types = requests.get(types_url, headers=headers)
    res_neighs = neighborhoods.json()['data']
    res_types = types.json()['data']
    if not res_types and not res_neighs:
        return redirect(url_for('.places_list'))
    names_neighs = []
    names_types = []
    for item in res_neighs:
        names_neighs.append(item['name'])
    for item in res_types:
        names_types.append(item['type_name'])
    form.neighborhood.choices = names_neighs
    form.place_type.choices = names_types
    if request.method == "POST":
        api_url = "http://localhost:8000/api/v1/places"
        data = {
            "place_type": {
                "type_name": form.place_type.data,
                "description": ""
            },
            "neighborhood": {
                "name": form.neighborhood.data
            },
            "name": form.name.data,
            "address": form.address.data,
            "description": form.description.data,
            "phone_number": form.phone.data,
            "grade": form.grade.data
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.places_list'))
    return render_template("placeForm.html", form=form, menu=menu, title="Добавление места")


@app.route('/place_edit/<place_id>', methods=["GET", "POST"])
def place_edit(place_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    form = placeForm(request.form, crsf=True)
    headers = {'Authorization': 'Bearer %s' % acces_token}
    neigh_url = "http://localhost:8000/api/v1/places/neighborhood"
    types_url = "http://localhost:8000/api/v1/places/types"
    neighborhoods = requests.get(neigh_url, headers=headers)
    types = requests.get(types_url, headers=headers)
    res_neighs = neighborhoods.json()['data']
    res_types = types.json()['data']
    if not res_types and not res_neighs:
        return redirect(url_for('.places_list'))
    names_neighs = []
    names_types = []
    for item in res_neighs:
        names_neighs.append(item['name'])
    for item in res_types:
        names_types.append(item['type_name'])
    form.neighborhood.choices = names_neighs
    form.place_type.choices = names_types
    if request.method == "GET":
        api_url = "http://localhost:8000/api/v1/places/"
        cur_place_data = requests.get(api_url + place_id, headers=headers)
        form.name.data = cur_place_data.json()['data'].get('name')
        form.address.data = cur_place_data.json()['data'].get('address')
        form.description.data = cur_place_data.json()['data'].get('description')
        form.phone.data = cur_place_data.json()['data'].get('phone_number')
        form.grade.data = cur_place_data.json()['data'].get('grade')
        form.neighborhood.data = cur_place_data.json()['data']['neighborhood'].get('name')
        form.place_type.data = cur_place_data.json()['data']['place_type'].get('type_name')
    if request.method == "POST":
        api_url = "http://localhost:8000/api/v1/places/"
        data = {
            "place_type": {
                "type_name": form.place_type.data,
                "description": ""
            },
            "neighborhood": {
                "name": form.neighborhood.data
            },
            "name": form.name.data,
            "address": form.address.data,
            "description": form.description.data,
            "phone_number": form.phone.data,
            "grade": form.grade.data
        }
        response = requests.put(api_url + place_id, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.places_list'))
    return render_template("placeForm.html", form=form, menu=menu, title="Изменение места")


@app.route('/place_del/<place_id>', methods=["GET", "DELETE"])
def delete_place(place_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + place_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('.places_list'))
