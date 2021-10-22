"""
This module contains a test for creating a device.
Its coverage is superseded by test_devices_crud.py and could be deleted.
However, it remains in this project to serve as example code.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import requests


# --------------------------------------------------------------------------------
# Create Tests
# --------------------------------------------------------------------------------

def test_create_device(base_url, session):

  # Test data
  thermostat_data = {
    'name': 'Main Thermostat',
    'location': 'Living Room',
    'type': 'Thermostat',
    'model': 'ThermoBest 3G',
    'serial_number': 'TB3G-12345'
  }

  # Create
  device_url = base_url.concat('/devices/')
  post_response = session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify create
  assert post_response.status_code == 200
  assert 'id' in post_data
  assert isinstance(post_data['id'], int)
  thermostat_data['id'] = post_data['id']
  thermostat_data['owner'] = session.auth[0]
  assert post_data == thermostat_data

  # Retrieve
  get_response = session.get(device_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  get_devices = [d for d in get_data['devices']
                   if d['id'] == post_data['id']]
  assert len(get_devices) == 1
  assert get_devices[0] == post_data
