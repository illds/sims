from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    name = StringField('Job name', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField('Done')
