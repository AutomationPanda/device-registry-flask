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
from .docs import auto
from .errors import NotFoundError, UserUnauthorizedError
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


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@devices.route('/devices/', methods=['GET'])
@auto.doc()
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
@auto.doc()
@multi_auth.login_required
def devices_post():
  """
  Adds a new device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = Device.from_json(request.json, username)
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['GET'])
@auto.doc()
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
@auto.doc()
@multi_auth.login_required
def device_id_patch_put(id):
  """
  Updates a device owned by the user.
  Requires authentication.
  """

  username = multi_auth.current_user()
  device = query_device(id, username)
  
  if request.method == 'PATCH':
    device.patch_from_json(request.json)
  else:
    device.update_from_json(request.json)
  
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['DELETE'])
@auto.doc()
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
@auto.doc()
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
