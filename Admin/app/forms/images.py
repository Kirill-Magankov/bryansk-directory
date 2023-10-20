from flask_wtf import FlaskForm as form
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class imageForm(form):
    image = FileField('image', validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(imageForm, self).__init__(*args, **kwargs)
