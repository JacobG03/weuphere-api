from app import app, db
from app.models import User
from .schemas import CreateRegisterSchema
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies


api = Blueprint('api', __name__, url_prefix='/api')

@api.after_request
def refresh_expiring_jwts(response):
  try:
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
        access_token = create_access_token(identity=get_jwt_identity())
        set_access_cookies(response, access_token)
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


registerSchema = CreateRegisterSchema()

@api.post('/auth/register')
def register():
  data = request.get_json(silent=True)
  if data == None:
    return jsonify({
      'message': "'form' required",
      'form': {
        'username': None,
        'email': None,
        'password': None,
        'password2': None,
      }
    }), 400
  
  errors = registerSchema.validate(data)
  if errors:
    return jsonify({
      'success': False,
      'errors': errors
    }), 400

  elif data['password'] != data['password2']:
    return jsonify({
      'success': False,
      'errors': {
        'password': ['Passwords must match'],
        'password2': ['Passwords must match']
      }
    }), 400


  #? If all OK
  user = User(
    username=data['username'],
    email=data['email'],
    password=generate_password_hash(data['password'], method='sha256'),
  )

  db.session.add(user)
  db.session.commit()

  return jsonify({
    'success': True,
    'message': 'Registered successfully'
  }), 200


#? post /api/auth/login
@api.post('/auth/login')
def login():
  data = request.get_json()
  if not data or not data['email'] or not data['password']:
    return make_response('could not verify', 401, {'Authentication': 'login required"'})   

  user = User.query.filter_by(email=data['email']).first()  
  if check_password_hash(user.password, data['password']):
    access_token = create_access_token(identity=[user.username, user.id])
    set_access_cookies(jsonify({'token' : access_token}), access_token)
    return jsonify({'token' : access_token})

  return make_response('could not verify',  401, {'Authentication': '"login required"'})


@api.get('/auth/refresh')
@jwt_required(locations=['headers', 'cookies'])
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity)
  return jsonify(access_token=access_token)


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


