import requests
from flask import request, render_template, make_response, redirect, url_for

from app import app
from app.constant import api_url


@app.route('/logout', methods=["GET", "POST"])
def logout():
    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect(url_for('.login'))
    headers = {'Authorization': 'Beares %s' % access_token}
    requests.post(api_url + 'users/logout', headers=headers)
    resp = make_response(redirect(url_for('.login')))
    resp.delete_cookie('accces_token')
    return resp
