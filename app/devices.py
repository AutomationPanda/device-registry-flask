from . import db
from .auth import multi_auth
from .errors import not_found
from .models import Device

from flask import Blueprint, request, jsonify


devices = Blueprint('devices', __name__)


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


# @devices.route('/devices/<int:id>/report')
# def devices_id_report(id):
#   return str(id)


# @devices.route('/devices/<int:id>/image')
# def devices_id_image(id):
#   return str(id)