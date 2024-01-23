from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange

from sims.models import VehicleType, Color


class VehicleForm(FlaskForm):
    plate = StringField('Plate №', validators=[DataRequired()])
    type = SelectField('Type', choices=[(vehicle_type.value, vehicle_type.value) for vehicle_type in VehicleType],
                       validators=[DataRequired()])
    color = SelectField('Color', choices=[(color.value, color.value) for color in Color],
                       validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired(), NumberRange(min=-450, max=450)])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired(), NumberRange(min=-200, max=200)])
    submit = SubmitField('Done')
