from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired()])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired()])
    submit = SubmitField('Done')
