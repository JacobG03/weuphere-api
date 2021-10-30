import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  # General
  SECRET_KEY = os.environ.get('SECRET_KEY') or '12uh3qadsjn-zxckey'

  # Database config
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_IRL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_TYPE = 'filesystem'

  # JWT config
  JWT_COOKIE_SECURE = False
  JWT_TOKEN_LOCATION = ["cookies"]
  JWT_SECRET_KEY = "supa-dupa-secreeet"
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


# API customizable settings
class ApiConfig(object):
  USERS_MAX_QUERY = 500