"""
This module provides a blueprint for authentication support.
Most resources (but not all) in this app require authentication.

Authentication may be handled two ways:
1. Basic HTTP authentication (username/password)
2. Token authentication (Bearer)

The username and password come from 'users', which gets values from the config.
In a *real* app, the database should store users and passwords.

Call the "/authenticate/" resource to get an authentication token.
Tokens expire after 1 hour (unless otherwise configured).
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import jwt

from . import users
from .errors import unauthorized

from flask import Blueprint, current_app, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import check_password_hash


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


# --------------------------------------------------------------------------------
# Authentication Token Functions
# --------------------------------------------------------------------------------

def serialize_token(username):
  secret_key = current_app.config['SECRET_KEY']
  token = jwt.encode({"username": username}, secret_key, algorithm="HS256")
  return token


def deserialize_token(token):
  try:
    secret_key = current_app.config['SECRET_KEY']
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
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

@auth.route('/authenticate/', methods=['GET'])
@basic_auth.login_required
def authenticate():
  """
  Uses HTTP basic authentication to generate an authentication token.
  Any resource that requires authentication can use either basic auth or this token.
  """
  
  token = serialize_token(basic_auth.current_user())
  response = {'token': token}
  return jsonify(response)