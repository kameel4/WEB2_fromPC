from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class MealOrder(FlaskForm):
    klass = StringField("Класс", validators=[DataRequired()])
    bufet = IntegerField("Кол-во порций буфета:")
    hot_meal = IntegerField("Кол-во порций горячего питания:")
    submit = SubmitField('Отправить заявку')
