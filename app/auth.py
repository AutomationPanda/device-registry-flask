"""
This module provides a blueprint for authentication support.
Most resources (but not all) in this app require authentication.

Authentication may be handled two ways:
1. Basic HTTP authentication (username/password)
2. Token authentication (Bearer)

The username and password are hardcoded to "pythonista" and "I<3testing".
In a *real* app, the database should store users and passwords.

Call the "/authenticate/" resource to get an authentication token.
Tokens expire after 1 hour (unless otherwise configured).
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from .errors import unauthorized

from flask import Blueprint, current_app, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWS
from werkzeug.security import generate_password_hash, check_password_hash


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

auth = Blueprint('auth', __name__)


# --------------------------------------------------------------------------------
# Authenticators
# https://github.com/miguelgrinberg/Flask-HTTPAuth/blob/main/examples/multi_auth.py
# --------------------------------------------------------------------------------

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(basic_auth, token_auth)

users = {
  'pythonista': generate_password_hash('I<3testing')
}


# --------------------------------------------------------------------------------
# Authentication Token Functions
# --------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------------
# Authentication Verification Functions
# --------------------------------------------------------------------------------

@basic_auth.verify_password
def verify_password(username, password):
  if username in users:
      if check_password_hash(users.get(username), password):
          return username


@token_auth.verify_token
def verify_token(token):
  if username := deserialize_token(token):
    return username


# --------------------------------------------------------------------------------
# Authentication Error Handlers
# --------------------------------------------------------------------------------

@basic_auth.error_handler
@token_auth.error_handler
def auth_error():
  return unauthorized('Invalid credentials')


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@auth.route('/authenticate/')
@basic_auth.login_required
def authenticate():
  token = serialize_token(basic_auth.current_user())
  response = {'token': token.decode('ascii')}
  return jsonify(response)