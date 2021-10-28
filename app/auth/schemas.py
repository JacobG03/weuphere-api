from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
import re
from app.models import User
from sqlalchemy import func


class CreateRegisterSchema(Schema):
  username = fields.Str(required=True, validate=Length(3, 64))
  email = fields.Str(required=True,  validate=Length(3, 128))
  password = fields.Str(required=True, validate=Length(4, 128))
  password2 = fields.Str(required=True, validate=[Length(4, 128)])


  @validates('username')
  def validateUsername(self, value):
    username_regex = re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{3,64}(?<![-._])$')
    if username_regex.match(value) == None:
      raise ValidationError('username not valid')
    #* Case insensitive query filter
    elif User.query.filter(func.lower(User.username) == func.lower(value)).first():
      raise ValidationError('username taken')


  @validates('email')
  def validateEmail(self, value):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if email_regex.match(value) == None:
      raise ValidationError('email not valid')
    #* Case insensitive query filter
    elif User.query.filter(func.lower(User.email) == func.lower(value)).first():
      raise ValidationError('email taken')