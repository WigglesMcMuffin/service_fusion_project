from flask import flash
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Required, Regexp, Optional
from flask_app.models.base import User

class UserForm(Form):
  first_name = StringField('First Name', validators=[Required()])
  last_name = StringField('Last Name', validators=[Required()])
  date_of_birth = DateField('Date of Birth', validators=[Optional()])
  zip_code = StringField('Zip Code', validators=[
                                                  Required(),
                                                  Regexp(
                                                    '[0-9]{5}',
                                                    message='Zip code must contain only 5 number'
                                                  )])
