"""
This module provides a blueprint for device resources.
The resources cover basic CRUD operations.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import io

from . import db
from .auth import multi_auth
from .errors import NotFoundError, UserUnauthorizedError, ValidationError
from .models import Device

from flask import Blueprint, jsonify, request
from werkzeug.utils import send_file


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

devices = Blueprint('devices', __name__)


# --------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------

def query_device(id, username):
  device = Device.query.filter_by(id=id).first()
  
  if not device:
    raise NotFoundError()
  elif device.owner != username:
    raise UserUnauthorizedError()
  
  return device


def get_json_from_request(request):
  try:
    data = request.json
  except:
    raise ValidationError(f'request body is missing all fields')

  return data


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@devices.route('/devices/', methods=['GET'])
@multi_auth.login_required
def devices_get():
  """
  Gets a list of all devices owned by the user.
  Requires authentication.
  """
  
  filter_args = dict()
  filter_args['owner'] = multi_auth.current_user()

  for field in ['id', 'name', 'location', 'type', 'model', 'serial_number']:
    if value := request.args.get(field):
      filter_args[field] = value

  ds = Device.query.filter_by(**filter_args)
  device_dict = {'devices': [device.to_json() for device in ds]}
  return jsonify(device_dict)


@devices.route('/devices/', methods=['POST'])
@multi_auth.login_required
def devices_post():
  """
  Adds a new device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  data = get_json_from_request(request)
  device = Device.from_json(data, username)
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['GET'])
@multi_auth.login_required
def device_id_get(id):
  """
  Gets a device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = query_device(id, username)
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['PATCH', 'PUT'])
@multi_auth.login_required
def device_id_patch_put(id):
  """
  Updates a device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = query_device(id, username)
  data = get_json_from_request(request)
  
  if request.method == 'PATCH':
    device.patch_from_json(data)
  else:
    device.update_from_json(data)
  
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['DELETE'])
@multi_auth.login_required
def device_id_delete(id):
  """
  Deletes a device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = query_device(id, username)
  db.session.delete(device)
  db.session.commit()
  return jsonify(dict())


@devices.route('/devices/<int:id>/report', methods=['GET'])
@multi_auth.login_required
def devices_id_report_get(id):
  """
  Prints a text-based report for a device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = query_device(id, username)

  report = io.BytesIO()
  report.write(bytes(f'ID: {device.id}\n', 'ascii'))
  report.write(bytes(f'Name: {device.name}\n', 'ascii'))
  report.write(bytes(f'Location: {device.location}\n', 'ascii'))
  report.write(bytes(f'Type: {device.type}\n', 'ascii'))
  report.write(bytes(f'Model: {device.model}\n', 'ascii'))
  report.write(bytes(f'Serial Number: {device.serial_number}\n', 'ascii'))
  report.write(bytes(f'Owner: {device.owner}\n', 'ascii'))
  report.seek(0)

  return send_file(
    report,
    request.environ,
    mimetype='text/plain',
    download_name=f'{device.name}.txt',
    as_attachment=True)
