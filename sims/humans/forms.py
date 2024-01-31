from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

from sims.models import Gender


class HumanForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Regexp(r'^[A-Za-z]+$', message='Name should contain only letters.')])
    surname = StringField('Surname', validators=[DataRequired(), Regexp(r'^[A-Za-z]+$',
                                                                        message='Surname should contain only letters.')])
    gender = SelectField('Gender', choices=[(gender.value, gender.value) for gender in Gender],
                         validators=[DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0, max=100)])
    job = SelectField('Job', coerce=int)
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired(), NumberRange(min=-450, max=450)])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired(), NumberRange(min=-200, max=200)])
    submit = SubmitField('Done')


class HumanJobForm(FlaskForm):
    job = SelectField('Job', coerce=int)
    submit = SubmitField('Done')


class HumanCoordinatesForm(FlaskForm):
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired(), NumberRange(min=-450, max=450)])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired(), NumberRange(min=-200, max=200)])
    submit = SubmitField('Done')
