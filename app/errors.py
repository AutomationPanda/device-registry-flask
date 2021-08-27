"""
This module provides error handlers for this Flask app.
Error handlers must be overridden to provide JSON responses.
This module also provides a ValidationError exception class.
Any ValidationError exceptions yield a "400 Bad Request" response.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from flask import Blueprint, jsonify


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

errors = Blueprint('errors', __name__)


# --------------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------------

class NotFoundError(Exception):
  def __str__(self):
    return 'not found'


class UserUnauthorizedError(Exception):
  def __str__(self):
    return 'current user is not authorized to access this resource'


class ValidationError(ValueError):
  pass


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@errors.app_errorhandler(400)
@errors.app_errorhandler(ValidationError)
def bad_request(e):
  response = jsonify({'error': 'bad request', 'message': str(e)})
  response.status_code = 400
  return response


@errors.app_errorhandler(401)
def unauthorized(e):
  response = jsonify({'error': 'unauthorized', 'message': str(e)})
  response.status_code = 401
  return response


@errors.app_errorhandler(403)
@errors.app_errorhandler(UserUnauthorizedError)
def forbidden(e):
  response = jsonify({'error': 'forbidden', 'message': str(e)})
  response.status_code = 403
  return response


@errors.app_errorhandler(404)
@errors.app_errorhandler(NotFoundError)
def not_found(e=None):
  response = jsonify({'error': 'not found'})
  response.status_code = 404
  return response


@errors.app_errorhandler(405)
def method_not_allowed(e):
  response = jsonify({'error': 'method not allowed', 'valid_methods': e.valid_methods})
  response.status_code = 405
  return response


@errors.app_errorhandler(500)
def internal_server_error(e):
  response = jsonify({'error': 'internal server error'})
  response.status_code = 500
  return response