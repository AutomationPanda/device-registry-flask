"""
This module provides support for testing devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import warnings


# --------------------------------------------------------------------------------
# Verification Functions
# --------------------------------------------------------------------------------

def verify_device_data(actual, expected):

  # Verify ID
  if 'id' in expected:
    assert actual['id'] == expected['id']
  else:
    assert isinstance(actual['id'], int)
  
  # Verify field length
  fields = ['name', 'location', 'type', 'model', 'serial_number', 'owner']
  assert len(actual) == len(fields) + 1

  # Verify field values
  for field in fields:
    assert field in actual
    assert actual[field] == expected[field]


def verify_devices(actual_list, expected_list, excluding=None):
  
  # Verify the device count
  assert len(actual_list) >= len(expected_list)

  # Create a mapping of IDs to data for actual devices
  # This will make verifications much more efficient
  actual_map = {device['id']: device for device in actual_list}

  # Verify each expected device is in the actual list
  # Note that other devices could also be in the actual list, and that's okay
  for expected in expected_list:
    assert expected['id'] in actual_map
    actual = actual_map[expected['id']]
    verify_device_data(actual, expected)
  
  # Verify excluded device IDs are not in the actual list
  if excluding:
    for excluded in excluding:
      assert excluded not in actual_map
      

# --------------------------------------------------------------------------------
# Class: DeviceCreator
# --------------------------------------------------------------------------------

class DeviceCreator:

  def __init__(self, base_url):
    self.base_url = base_url
    self.created = dict()


  def create(self, session, request_data):

    # Create
    device_url = self.base_url.concat('/devices/')
    post_response = session.post(device_url, json=request_data)
    post_data = post_response.json()
    
    # Verify create
    assert post_response.status_code == 200
    request_data['owner'] = session.auth[0]
    verify_device_data(post_data, request_data)

    # Register created device with its session
    self.created[post_data['id']] = session

    # Return data
    return post_data


  def delete(self, session, id):

    # Delete
    delete_url = self.base_url.concat(f'/devices/{id}')
    delete_response = session.delete(delete_url)
    
    # Issue warning for delete failure
    if delete_response.status_code != 200:
      warnings.warn(UserWarning(f'Deleting device with id={id} failed'))
  

  def remove(self, id):
    del self.created[id]
  

  def cleanup(self):
    for id in self.created:
      self.delete(self.created[id], id)
    self.created = dict()
