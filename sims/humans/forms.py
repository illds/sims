from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

from sims.models import Gender, Job


class HumanForm(FlaskForm):
    MROT = 19242
    name = StringField('Name',
                       validators=[DataRequired(), Regexp(r'^[A-Za-z]+$', message='Name should contain only letters.')])
    surname = StringField('Surname', validators=[DataRequired(), Regexp(r'^[A-Za-z]+$',
                                                                        message='Surname should contain only letters.')])
    gender = SelectField('Gender', choices=[(gender.value, gender.value) for gender in Gender],
                         validators=[DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0, max=100)])
    salary = IntegerField('Salary', validators=[InputRequired(), NumberRange(min=19242, max=1000000)])
    job = SelectField('Job', choices=[(job.value, job.value) for job in Job],
                      validators=[DataRequired()])
    x_coordinate = IntegerField('X coordinate', validators=[DataRequired(), NumberRange(min=-450, max=450)])
    y_coordinate = IntegerField('Y coordinate', validators=[DataRequired(), NumberRange(min=-200, max=200)])
    submit = SubmitField('Done')
