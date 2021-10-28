from app import app, db
from app.models import User
from flask import request, jsonify, make_response, Blueprint
from datetime import datetime, timezone, timedelta

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies


api = Blueprint('api', __name__, url_prefix='/api')


#? Refreshes token on every request with token expriring in less than < 30 minutes 

@api.after_request
def refresh_expiring_jwts(response):
  try:
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
      access_token = create_access_token(identity=get_jwt_identity())
      set_access_cookies(response, access_token)
      print('new cookie')
    return response
  except (RuntimeError, KeyError):
    # Case where there is not a valid JWT. Just return the original respone
    return response

@api.get('/')
def index():
  url = 'http://localhost:5000/api'
  return jsonify({
    'message': 'Greetings! The API seems to be working..',
    'routes': [
      f'{url}/auth/register', 
      f'{url}/auth/login', 
    ]
  })

#! get /api/user    (current_user) (:user === some other user)




#* get /api/:user     (:user or :id)
#* /api/:user/profile
#* /api/:user/history   etc..


#! /api/user/settings
#* /api/user/settings/delete_account


#! get /api/users     returns all /users routes

@api.get('/users')
@jwt_required(locations=['headers', 'cookies'])
def users():
  return jsonify({
    'message': 'Working'
  })

#* get /api/users/1/500  default by id  (500 being the limit)
#* get /api/users/1/500?sort=new   // newest users
#* get /api/users/1/500?sort=old   // oldest users    etc..


