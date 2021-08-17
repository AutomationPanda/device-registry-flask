from .errors import unauthorized

from flask import Blueprint, current_app, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWS
from werkzeug.security import generate_password_hash, check_password_hash


# https://github.com/miguelgrinberg/Flask-HTTPAuth/blob/main/examples/multi_auth.py


auth = Blueprint('auth', __name__)


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(basic_auth, token_auth)

users = {
  'pythonista': generate_password_hash('I<3testing')
}


def serialize_token(username):
  token = current_app.jws.dumps({'username': username})
  return token


def deserialize_token(token):
  try:
    data = current_app.jws.loads(token)
  except:
    return None
  if 'username' in data:
    return data['username']


@basic_auth.verify_password
def verify_password(username, password):
  if username in users:
      if check_password_hash(users.get(username), password):
          return username


@token_auth.verify_token
def verify_token(token):
  if username := deserialize_token(token):
    return username


@basic_auth.error_handler
@token_auth.error_handler
def auth_error():
  return unauthorized('Invalid credentials')


@auth.route('/authenticate/')
@basic_auth.login_required
def authenticate():
  token = serialize_token(basic_auth.current_user())
  response = {'token': token.decode('ascii')}
  return jsonify(response)