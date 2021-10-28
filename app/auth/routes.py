from app import db
from app.models import User
from .schemas import CreateRegisterSchema
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies

auth = Blueprint('auth', __name__, url_prefix='/auth')

registerSchema = CreateRegisterSchema()

@auth.post('/register')
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
@auth.post('/login')
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


@auth.get('/refresh')
@jwt_required(locations=['headers', 'cookies'])
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity)
  return jsonify(access_token=access_token)
