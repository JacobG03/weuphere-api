from app import app
from flask import request, jsonify
from app.models import User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None
    if 'x-access-tokens' in request.headers:
      token = request.headers['x-access-tokens']

    if not token:
      return jsonify({'message': 'a valid token is missing'})
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      current_user = User.query.filter_by(id=data['id']).first()
    except:
      return jsonify({'message': 'token is invalid'})

    return f(current_user, *args, **kwargs)
  return decorator