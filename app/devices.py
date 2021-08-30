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


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@devices.route('/devices/', methods=['GET'])
@multi_auth.login_required
def devices_get():
  username = multi_auth.current_user()
  ds = Device.query.filter_by(owner=username)
  device_dict = {'devices': [device.to_json() for device in ds]}
  return jsonify(device_dict)


@devices.route('/devices/', methods=['POST'])
@multi_auth.login_required
def devices_post():
  username = multi_auth.current_user()
  device = Device.from_json(request.json, username)
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['GET'])
@multi_auth.login_required
def device_id_get(id):
  username = multi_auth.current_user()
  device = query_device(id, username)
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['PATCH', 'PUT'])
@multi_auth.login_required
def device_id_patch_put(id):
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
@multi_auth.login_required
def device_id_delete(id):
  username = multi_auth.current_user()
  device = query_device(id, username)
  db.session.delete(device)
  db.session.commit()
  return jsonify(dict())


@devices.route('/devices/<int:id>/report', methods=['GET'])
@multi_auth.login_required
def devices_id_report_get(id):
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
