from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from marshmallow.validate import Length, Equal
import re


class CreateRegisterSchema(Schema):
  username = fields.Str(required=True, validate=Length(3, 64))
  email = fields.Str(required=True,  validate=Length(3, 128))
  password = fields.Str(required=True, validate=Length(4, 128))
  password2 = fields.Str(required=True, validate=[Length(4, 128)])


  @validates('username')
  def validateUsername(self, value):
    username_regex = re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$')
    if username_regex.match(value) == None:
      raise ValidationError('username not valid')


  @validates('email')
  def validateEmail(self, value):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if email_regex.match(value) == None:
      raise ValidationError('email not valid')
