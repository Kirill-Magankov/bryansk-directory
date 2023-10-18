from flask_wtf import FlaskForm as form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class authorizeForm(form):
    username = StringField('username', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    password = PasswordField('password',
                                  validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Авторизация')

    def __init__(self, *args, **kwargs):
        super(authorizeForm, self).__init__(*args, **kwargs)
