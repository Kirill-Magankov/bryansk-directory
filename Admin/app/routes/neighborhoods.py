import requests
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.constant import menu
from app.forms.neighborhoods import neighForm



@app.route('/neighborhoods')
def neighborhoods_list():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/neighborhood"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.get(api_url, headers=headers)
    if not response:
        response = {}
        return render_template('neighborhoods.html', menu=menu, title='Список типов мест',
                               neighborhoods_list=response)
    return render_template('neighborhoods.html', menu=menu, title='Список типов мест',
                           neighborhoods_list=response.json()['data'])



@app.route('/neighborhood_add', methods=["GET", "POST"])
def neighborhood_add():
    form = neighForm(request.form, crsf=True)
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    if form.validate_on_submit() and request.method == "POST":
        name = form.name.data
        api_url = "http://localhost:8000/api/v1/places/neighborhood"
        data = {
            "name": name
        }
        headers = {'Authorization': 'Bearer %s' % acces_token}
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.neighborhoods_list'))
        else:
            flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('neighForm.html', menu=menu, title='Добавление района', form=form)


@app.route('/neighborhood_edit/<neighborhood_id>', methods=["GET", "POST"])
def edit_neighborhood(neighborhood_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/neighborhood/"

    headers = {'Authorization': 'Bearer %s' % acces_token}
    form = neighForm(request.form, crsf=True)
    if request.method == "GET":
        cur_neigh = requests.get(api_url + neighborhood_id, headers=headers)
        form.name.data = cur_neigh.json()['data'].get('name')

    if request.method == "POST" and form.validate_on_submit():

        name = form.name.data

        data = {
            "name": name
        }

        response = requests.put(api_url + neighborhood_id, headers=headers, json=data)
        if response.status_code == 200:
            return redirect(url_for('.neighborhoods_list'))
        else:
            flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('neighForm.html', menu=menu, title='Редактирование типа места', form=form)


@app.route('/neighborhood_delete/<neighborhood_id>', methods=["GET", "DELETE"])
def delete_neighborhood(neighborhood_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:8000/api/v1/places/neighborhood/"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + neighborhood_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('.neighborhoods_list'))
