from flask_wtf import FlaskForm as form
from wtforms import SubmitField, StringField
from wtforms.widgets import TextArea


class feedbackForm(form):
    message = StringField('message',
                          widget=TextArea())
    submit = SubmitField('Отправить')

    def __init__(self, *args, **kwargs):
        super(feedbackForm, self).__init__(*args, **kwargs)
