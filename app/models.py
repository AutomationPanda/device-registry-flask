"""
This module provides database models.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from . import db
from .errors import ValidationError


# --------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------

class Device(db.Model):
  __tablename__ = 'devices'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  location = db.Column(db.String(64))
  type = db.Column(db.String(64))
  model = db.Column(db.String(64))
  serial_number = db.Column(db.String(16))
  owner = db.Column(db.String(64))

  @staticmethod
  def validate_full(json_data):
    """Raises a ValidationError if 'json_data' cannot be converted into a Device object."""

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
  def from_json(json_data, owner):
    """Creates a Device object based on the 'json_data' dictionary."""
    Device.validate_full(json_data)
    return Device(owner=owner, **json_data)

  def to_json(self):
    """Creates a JSON-compatible dictionary for this Device object's values."""
    return {
      'id': self.id,
      'name': self.name,
      'location': self.location,
      'type': self.type,
      'model': self.model,
      'serial_number': self.serial_number,
      'owner': self.owner
    }

  def update_from_json(self, json_data):
    """Updates this Device object using values from the 'json_data' dictionary."""
    Device.validate_full(json_data)
    self.name = json_data['name']
    self.location = json_data['location']
    self.type = json_data['type']
    self.model = json_data['model']
    self.serial_number = json_data['serial_number']

  def patch_from_json(self, json_data):
    """Patches this Device object's 'name' and 'location' fields from 'json_data'."""
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
