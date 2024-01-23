from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

from sims.models import PetType, Gender


class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[(pet_type.value, pet_type.value) for pet_type in PetType],
                       validators=[DataRequired()])
    gender = SelectField('Gender', choices=[(gender.value, gender.value) for gender in Gender],
                       validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired()])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired()])
    submit = SubmitField('Done')
