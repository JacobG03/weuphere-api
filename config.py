import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  # General
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'

  # Database config
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_IRL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_TYPE = 'filesystem'