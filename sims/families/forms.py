from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired


class FamilyForm(FlaskForm):
    name = StringField('Family Name', validators=[DataRequired()])
    submit = SubmitField('Done')
