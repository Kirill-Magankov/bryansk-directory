from flask_wtf import FlaskForm as form
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class reviewForm(form):
    date = DateField('date', validators=[DataRequired(message='Обязательное поле')])
    author_name = StringField('author_name', validators=[Length(min=4, max=255)])
    description = StringField('description',
                              validators=[Length(min=4, max=255)],
                              widget=TextArea())
    url = StringField('url', validators=[Length(min=4, max=255)])
    grade = FloatField('grade', validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(reviewForm, self).__init__(*args, **kwargs)
