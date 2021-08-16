import click
import os
import time

from flask import Flask, request, jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
start_time = time.time()

db_path = os.path.join(app.root_path, 'registry_data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Device(db.Model):
  __tablename__ = 'devices'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  location = db.Column(db.String(64))
  type = db.Column(db.String(64))
  model = db.Column(db.String(64))
  serial_number = db.Column(db.String(16))

  @staticmethod
  def validate_full(json_data):
    if not json_data:
      raise ValidationError(f'The device is missing all data')

    valid_fields = ['name', 'location', 'type', 'model', 'serial_number']
    missing_fields = [key for key in valid_fields if key not in json_data]
    if missing_fields:
      raise ValidationError(f'The device has missing fields: {", ".join(missing_fields)}')

    invalid_fields = [key for key in json_data if key not in valid_fields]
    if invalid_fields:
      raise ValidationError(f'The device has invalid fields: {", ".join(invalid_fields)}')

  @staticmethod
  def from_json(json_data):
    Device.validate_full(json_data)
    return Device(**json_data)

  def to_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'location': self.location,
      'type': self.type,
      'model': self.model,
      'serial_number': self.serial_number
    }

  def update_from_json(self, json_data):
    Device.validate_full(json_data)
    self.name = json_data['name']
    self.location = json_data['location']
    self.type = json_data['type']
    self.model = json_data['model']
    self.serial_number = json_data['serial_number']

  def patch_from_json(self, json_data):
    if not json_data:
        raise ValidationError(f'The request is missing all data')

    invalid_keys = [key for key in json_data.keys() if key != 'name' and key != 'location']
    if invalid_keys:
      raise ValidationError(f'Invalid fields: {", ".join(invalid_keys)}')

    if 'name' in json_data:
      self.name = json_data['name']
    if 'location' in json_data:
      self.location = json_data['location']

  def __repr__(self):
    return f'<Device {self.name}>'


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.drop_all()
    db.create_all()
    device = Device(name='Downstairs Thermostat', location='Living Room', type='Thermostat', model='Nest 3G', serial_number='12345')
    db.session.add(device)
    db.session.commit()
    click.echo('Initialized the database with fresh data.')

app.cli.add_command(init_db_command)


class ValidationError(ValueError):
  pass


@app.errorhandler(400)
@app.errorhandler(ValidationError)
def bad_request(e):
  response = jsonify({'error': 'bad request', 'message': str(e)})
  response.status_code = 400
  return response


@app.errorhandler(403)
def forbidden(e):
  response = jsonify({'error': 'forbidden', 'message': str(e)})
  response.status_code = 403
  return response


@app.errorhandler(404)
def not_found(e):
  response = jsonify({'error': 'not found'})
  response.status_code = 404
  return response


@app.errorhandler(405)
def not_found(e):
  response = jsonify({'error': 'method not allowed', 'valid_methods': e.valid_methods})
  response.status_code = 405
  return response


@app.errorhandler(500)
def internal_server_error(e):
  response = jsonify({'error': 'internal server error'})
  response.status_code = 500
  return response


@app.route('/')
def index():
  return 'This is a device registry REST API.'


@app.route('/status/')
def status():
  response = {
    'online': True,
    'uptime': round(time.time() - start_time, 3)
  }
  return jsonify(response)


@app.route('/devices/', methods=['GET'])
def get_devices():
  devices = Device.query.all()
  device_dict = {'devices': [device.to_json() for device in devices]}
  return jsonify(device_dict)


@app.route('/devices/', methods=['POST'])
def post_devices():
  device = Device.from_json(request.json)
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


@app.route('/devices/<int:id>', methods=['GET'])
def get_device_id(id):
  device = Device.query.filter_by(id=id).first()
  if not device:
    return not_found(None)
  else:
    return jsonify(device.to_json())


@app.route('/devices/<int:id>', methods=['PATCH', 'PUT'])
def patch_put_device_id(id):
  device = Device.query.filter_by(id=id).first()
  if not device:
    return not_found(None)
  
  if request.method == 'PATCH':
    device.patch_from_json(request.json)
  else:
    device.update_from_json(request.json)
  
  db.session.add(device)
  db.session.commit()
  return jsonify(device.to_json())


# @app.route('/devices/<int:id>/report')
# def devices_id_report(id):
#   return str(id)


# @app.route('/devices/<int:id>/image')
# def devices_id_image(id):
#   return str(id)
