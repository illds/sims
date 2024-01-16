from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HouseForm(FlaskForm):
    owner_family = StringField("Family's surname", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    room_number = IntegerField('Room number', validators=[DataRequired()])
    floor_number = IntegerField('Floor number', validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired()])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired()])
    submit = SubmitField('Done')