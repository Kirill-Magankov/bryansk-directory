import requests
from flask import render_template, request, make_response, flash, redirect, url_for

from app import app
from app.constant import menu
from app.forms import authorize
from app.forms.authorize import authorizeForm


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    authForm = authorizeForm(request.form, crsf=False)
    if request.method == "POST" and authForm.validate_on_submit():
        username = authForm.username.data
        password = authForm.password.data
        remember_me = authForm.remember_me.data

        api_url = "http://localhost:8000/api/v1/users/login"

        data = {
            "username": username,
            "password": password,
            "remember_me": remember_me
        }
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print(access_token)
            resp = make_response(redirect(url_for('.places_list')))

            if remember_me:
                resp.set_cookie('access_token', access_token, max_age=60 * 60 * 24 * 15)
            else:
                resp.set_cookie('access_token', access_token)
            return resp

        else:
            flash("Неверные учётные данные. Пожалуйста, попробуйте снова.", "danger")

    return render_template('authForm.html', title='Авторизация', form=authForm)
