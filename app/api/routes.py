from app.models import User
from flask import config, request, jsonify, make_response, Blueprint
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies
from config import ApiConfig


api = Blueprint('api', __name__, url_prefix='/api')
config = ApiConfig()

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
@api.get('/<username>')
def user(username):
  user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
  if not user:
    return jsonify({
      'success': False
    })
  return jsonify({
    'user': {
      'username': user.username
    },
    'success': True
  })


#* /api/:user/profile
#* /api/:user/history   etc..


#! /api/user/settings
#* /api/user/settings/delete_account


#! get /api/users     returns all /users routes


@api.get('/users')
def users():
  return jsonify([
    '/users/<number>/<number>?sort=descending',
    '/users/<number>/<number>?sort=ascending'
  ])


@api.get('/users/<beg>/<end>')
def users_from_to(beg, end):
  users = []
  # Append users to list
  for i in range(int(beg), int(end) + 1):
    # Limit set by server
    if i == int(beg) + config.USERS_MAX_QUERY:
      break
    user = User.query.get(int(i))
    if user:
      users.append({
        'id': user.id,
        'username': user.username
      })
    
  # Check for sorting query


  return jsonify({
    'users': users,
    'message': f'{beg}, {end}, {request.args.get("sort")}'
  })

