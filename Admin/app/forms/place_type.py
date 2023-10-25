from flask_wtf import FlaskForm as form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class typeForm(form):
    type_name = StringField('type_name', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=50)])
    description = StringField('description',
                              widget=TextArea())
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(typeForm, self).__init__(*args, **kwargs)
