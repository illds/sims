from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

from sims.models import HouseType


class HouseForm(FlaskForm):
    type = SelectField('Type', choices=[(house_type.value, house_type.value) for house_type in HouseType],
                       validators=[DataRequired()])
    room_number = IntegerField('Room number', validators=[DataRequired()])
    floor_number = IntegerField('Floor number', validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired()])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired()])
    submit = SubmitField('Done')
