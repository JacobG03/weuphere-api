from app import app, db
from app.models import User
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app.decorators import token_required
from .schemas import CreateRegisterSchema


api = Blueprint('api', __name__, url_prefix='/api')

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


@api.get('/auth')
@token_required(refresh=True)
def auth(current_user):
  token = jwt.encode({'id' : current_user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
  return jsonify({'token' : token})

#? post /api/auth/register

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
    token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")

    return jsonify({'token' : token})

  return make_response('could not verify',  401, {'Authentication': '"login required"'})




#* get /api/:user     (:user or :id)
#* /api/:user/profile
#* /api/:user/history   etc..


#! /api/user/settings
#* /api/user/settings/delete_account


#! get /api/users     returns all /users routes

@api.get('/users')
@token_required
def users(current_user):
  return jsonify({
    'message': 'Working'
  })

#* get /api/users/1/500  default by id  (500 being the limit)
#* get /api/users/1/500?sort=new   // newest users
#* get /api/users/1/500?sort=old   // oldest users    etc..


