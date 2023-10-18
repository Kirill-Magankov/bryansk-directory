from flask_wtf import FlaskForm as form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class neighForm(form):
    name = StringField('name', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])

    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(neighForm, self).__init__(*args, **kwargs)
