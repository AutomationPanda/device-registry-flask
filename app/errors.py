from flask import Blueprint, jsonify


errors = Blueprint('errors', __name__)


class ValidationError(ValueError):
  pass


@errors.errorhandler(400)
@errors.errorhandler(ValidationError)
def bad_request(e):
  response = jsonify({'error': 'bad request', 'message': str(e)})
  response.status_code = 400
  return response


@errors.errorhandler(401)
def unauthorized(e):
  response = jsonify({'error': 'unauthorized', 'message': str(e)})
  response.status_code = 401
  return response


@errors.errorhandler(403)
def forbidden(e):
  response = jsonify({'error': 'forbidden', 'message': str(e)})
  response.status_code = 403
  return response


@errors.errorhandler(404)
def not_found(e):
  response = jsonify({'error': 'not found'})
  response.status_code = 404
  return response


@errors.errorhandler(405)
def not_found(e=None):
  response = jsonify({'error': 'method not allowed', 'valid_methods': e.valid_methods})
  response.status_code = 405
  return response


@errors.errorhandler(500)
def internal_server_error(e):
  response = jsonify({'error': 'internal server error'})
  response.status_code = 500
  return response