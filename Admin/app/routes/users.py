import requests
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.constant import menu, api_url
from app.forms.users import userForm


@app.route('/users')
def users_list():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % acces_token}
    try:
        response = requests.get(api_url + "users", headers=headers).json()['data']
    except KeyError:
        response = {}
    return render_template('users.html', menu=menu, title='Список пользователей', user_list=response)


@app.route('/user_add', methods=["GET", "POST"])
def user_add():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    form = userForm(request.form, crsf=True)
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
            headers = {'Authorization': 'Bearer %s' % acces_token}
            response = requests.post(api_url + "users", headers=headers, json=data)
            if response.status_code == 200:
                return redirect(url_for('users_list'))
            else:
                flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('regForm.html', menu=menu, title='Добавление пользователя', form=form)


@app.route('/user_edit/<user_id>', methods=["GET", "POST"])
def user_edit(user_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    form = userForm(request.form, crsf=True)
    headers = {'Authorization': 'Bearer %s' % acces_token}
    if request.method == "GET":
        cur_user = requests.get(api_url + "users/" + user_id, headers=headers)
        form.username.data = cur_user.json()['data'].get('username')
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        pwd2 = form.password_repeat.data
        if pwd == pwd2:
            print("Совпали")
            data = {
                "username": username,
                "password": pwd
            }

            response = requests.put(api_url + "users/с"+ user_id, headers=headers, json=data)
            if response.status_code == 200:
                return redirect(url_for('users_list'))
            else:
                flash("Произошла ошибка, попробуйте позже", "danger")

        else:

            flash("Введенные пароли не совпадают", "danger")
    return render_template('regForm.html', menu=menu, title='Редактирование пользователя', form=form)


@app.route('/user_del/<user_id>', methods=["GET", "DELETE"])
def delete_user(user_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + "users/" + user_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('users_list'))
