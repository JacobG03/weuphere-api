from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
from flask import request, jsonify, make_response
import jwt
import datetime
from app.decorators import token_required


@app.get('/api')
def api():
  return {
    'message': 'Greetings! The API seems to be working..',
    'routes': []
  }

#! get /api/user    (current_user) (:user === some other user)



#? post /api/user/register

@app.post('/api/user/register')
def register():
  data = request.get_json()
  hashed_password = generate_password_hash(data['password'], method='sha256')

  user = User(
    name=data['name'],
    surname=data['surname'],
    email=data['email'],
    password=hashed_password,
  )

  db.session.add(user)
  db.session.commit()

  return jsonify({
    'success': True,
    'message': 'Registered successfully'
  })


#? post /api/user/login
@app.post('/api/user/login')
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

@app.get('/api/users')
@token_required
def users(current_user):
  return jsonify({
    'message': 'Working'
  })

#* get /api/users/1/500  default by id  (500 being the limit)
#* get /api/users/1/500?sort=new   // newest users
#* get /api/users/1/500?sort=old   // oldest users    etc..


