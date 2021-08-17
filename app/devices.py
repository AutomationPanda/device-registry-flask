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
from .errors import not_found
from .models import Device

from flask import Blueprint, request, jsonify
from werkzeug.utils import send_file


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

devices = Blueprint('devices', __name__)


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@devices.route('/devices/', methods=['GET'])
@multi_auth.login_required
def get_devices():
  ds = Device.query.all()
  device_dict = {'devices': [device.to_json() for device in ds]}
  return jsonify(device_dict)


@devices.route('/devices/', methods=['POST'])
@multi_auth.login_required
def post_devices():
  device = Device.from_json(request.json)
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['GET'])
@multi_auth.login_required
def get_device_id(id):
  device = Device.query.filter_by(id=id).first()
  if not device:
    return not_found()
  else:
    return jsonify(device.to_json())


@devices.route('/devices/<int:id>', methods=['PATCH', 'PUT'])
@multi_auth.login_required
def patch_put_device_id(id):
  device = Device.query.filter_by(id=id).first()
  if not device:
    return not_found()
  
  if request.method == 'PATCH':
    device.patch_from_json(request.json)
  else:
    device.update_from_json(request.json)
  
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@devices.route('/devices/<int:id>/report', methods=['GET'])
@multi_auth.login_required
def devices_id_report(id):
  device = Device.query.filter_by(id=id).first()
  if not device:
    return not_found()

  report = io.BytesIO()
  report.write(bytes(f'ID: {device.id}\n', 'ascii'))
  report.write(bytes(f'Name: {device.name}\n', 'ascii'))
  report.write(bytes(f'Location: {device.location}\n', 'ascii'))
  report.write(bytes(f'Type: {device.type}\n', 'ascii'))
  report.write(bytes(f'Model: {device.model}\n', 'ascii'))
  report.write(bytes(f'Serial Number: {device.serial_number}\n', 'ascii'))
  report.seek(0)

  return send_file(
    report,
    request.environ,
    mimetype='text/plain',
    download_name=f'{device.name}.txt',
    as_attachment=True)
