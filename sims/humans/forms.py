from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

from sims.models import Gender, Job


class HumanForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[(gender.value, gender.value) for gender in Gender],
                         validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    job = SelectField('Job', choices=[(job.value, job.value) for job in Job],
                         validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired()])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired()])
    submit = SubmitField('Done')
