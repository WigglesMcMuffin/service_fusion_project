from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.String(36, convert_unicode=True), primary_key=True)
  first_name = db.Column(db.String(36))
  last_name = db.Column(db.String(36))
  date_of_birth = db.Column(db.Date, default=db.func.now())
  zip_code = db.Column(db.String(10))

  def __init__(self, first_name=None, last_name=None, date_of_birth=None, zip_code=None):
    self.id = uuid.uuid4()
    self.first_name = first_name
    self.last_name = last_name
    self.date_of_birth = date_of_birth
    self.zip_code = zip_code

  def __repr__(self):
    return '<User %s, %s - %s>' %(self.last_name, self.first_name, self.date_of_birth)


class UserSchema(ma.ModelSchema):
  class Meta:
    model = User
