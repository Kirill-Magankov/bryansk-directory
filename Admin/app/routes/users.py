import requests
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.constant import menu
from app.forms.users import userForm

users_test = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin"
    },
    {
        "id": 2,
        "username": "developer",
        "password": "developer"
    }
]


@app.route('/users')
def users_list():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:5000/api/v1/users"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.get(api_url, headers=headers)
    return render_template('users.html', menu=menu, title='Список пользователей', user_list=response.json()['data'])


@app.route('/user_add', methods=["GET", "POST"])
def user_add():
    form = userForm(request.form, crsf=True)
    acces_token = request.cookies.get('access_token')
    if form.validate_on_submit():
        if not acces_token:
            return redirect(url_for('.login'))
        username = form.username.data
        pwd = form.password.data
        pwd2 = form.password_repeat.data
        if pwd != pwd2:
            flash("Введенные пароли не совпадают", "danger")
        else:
            api_url = "http://localhost:5000/api/v1/users"
            data = {
                "username": username,
                "password": pwd
            }
            headers = {'Authorization': 'Bearer %s' % acces_token}
            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code == 200:
                return render_template("places.html", title="Список мест", menu=menu)
            else:
                flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('regForm.html', menu=menu, title='Добавление пользователя', form=form)


@app.route('/user_edit/<user_id>', methods=["GET", "POST"])
def user_edit(user_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:5000/api/v1/users/"
    form = userForm(request.form, crsf=True)
    headers = {'Authorization': 'Bearer %s' % acces_token}
    if request.method == "GET":
        cur_user = requests.get(api_url + user_id, headers=headers)
        form.username.data = cur_user.json()['data'].get('username')
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        pwd2 = form.password_repeat.data
        if pwd != pwd2:
            flash("Введенные пароли не совпадают", "danger")
        else:

            data = {
                "username": username,
                "password": pwd
            }

            response = requests.put(api_url + user_id, headers=headers, json=data)
            if response.status_code == 200:
                return redirect(url_for('.user_list'))
            else:
                flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('regForm.html', menu=menu, title='Редактирование пользователя', form=form)


@app.route('/user_del/<user_id>', methods=["GET", "DELETE"])
def delete_user(user_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('.login'))
    api_url = "http://localhost:5000/api/v1/users/"
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + user_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('.users_list'))
