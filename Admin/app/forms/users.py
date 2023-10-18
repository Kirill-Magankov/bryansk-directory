from flask_wtf import FlaskForm as form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class userForm(form):
    username = StringField('username', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    password = PasswordField('password',
                             validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    password_repeat = PasswordField('password_repeat',
                                    validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    submit = SubmitField('Сохранить')

    def init(self, *args, **kwargs):
        super(userForm, self).init(*args, **kwargs)