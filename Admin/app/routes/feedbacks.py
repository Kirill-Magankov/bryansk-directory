from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import smtplib
from flask import request, redirect, url_for, render_template, flash

from app import app
from app.constant import api_url, menu, SMTP_USERNAME, SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER
from app.forms.feedback import feedbackForm


@app.route('/feedback')
def feedback_list():
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % acces_token}
    try:
        response = requests.get(api_url + "feedbacks", headers=headers).json()['data']
    except KeyError:
        response = {}
    return render_template('feedbacks.html', menu=menu, title='Обратная связь', feedback_list=response)


@app.route('/send_feedback/<feedback_id>', methods=["GET", "POST"])
def send_feedback(feedback_id):
    form = feedbackForm(request.form, crsf=True)
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    if form.validate_on_submit() and request.method == "POST":
        headers = {'Authorization': 'Bearer %s' % acces_token}
        resp = requests.get(api_url + "feedbacks/" + feedback_id, headers=headers)
        message = form.message.data
        email = resp.json()['data'].get('email')
        data = {
            "status": "Closed",
            "comment": message
        }
        response = requests.put(api_url + "feedbacks/" + feedback_id, headers=headers, json=data)
        if form.validate_on_submit() and request.method == "POST":
            if response.status_code == 200:
                recipient_email = email
                sender_email = SMTP_USERNAME
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = 'Ответ на оставленное обращение'
                msg.attach(MIMEText(message, 'plain'))
                try:
                    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
                    server.ehlo()
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                    flash("Успешно отправлено на почту", "success")
                except smtplib.SMTPException as e:
                    flash(f'Произошла ошибка во время отправки: {e}', 'danger')
                    return redirect(url_for('feedback_list'))
            else:
                flash("Произошла ошибка, попробуйте позже", "danger")
    return render_template('feedbackForm.html', menu=menu, title='Обратная связь', form=form)


@app.route('/delete_feedback/<feedback_id>', methods=['GET', 'DELETE'])
def delete_feedback(feedback_id):
    acces_token = request.cookies.get('access_token')
    if not acces_token:
        return redirect(url_for('login'))
    headers = {'Authorization': 'Bearer %s' % acces_token}
    response = requests.delete(api_url + "feedbacks/" + feedback_id, headers=headers)
    if response.status_code == 200:
        return redirect(url_for('feedback_list'))
