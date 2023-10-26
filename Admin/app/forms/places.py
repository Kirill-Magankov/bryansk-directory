from flask_wtf import FlaskForm as form
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class filterForm(form):
    neighborhood = SelectField()
    place_type = SelectField()
    submit = SubmitField('Поиск')

    def __init__(self, *args, **kwargs):
        super(filterForm, self).__init__(*args, **kwargs)


class placeForm(form):
    name = StringField('name', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=100)])
    address = StringField('address', validators=[DataRequired(message='Обязательное поле'), Length(min=4, max=255)])
    description = StringField('description',
                              widget=TextArea())
    phone = StringField('phone', validators=[Length(max=11)])
    grade = FloatField('grade', validators=[DataRequired(message='Обязательное поле')])
    neighborhood = SelectField(validators=[DataRequired(message='Обязательное поле')])
    place_type = SelectField(validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(placeForm, self).__init__(*args, **kwargs)
