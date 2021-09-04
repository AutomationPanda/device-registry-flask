"""
This module provides support for testing devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import warnings


# --------------------------------------------------------------------------------
# Create Function
# --------------------------------------------------------------------------------

def create_device(base_url, user, session, request_data):

  # Create
  device_url = base_url.concat('/devices/')
  post_response = session.post(device_url, json=request_data)
  post_data = post_response.json()
  
  # Verify create
  assert post_response.status_code == 200
  request_data['owner'] = user.username
  verify_device_data(post_data, request_data)

  # Return data
  return post_data


# --------------------------------------------------------------------------------
# Delete Function
# --------------------------------------------------------------------------------

def delete_device(base_url, session, id):

    # Delete
    delete_url = base_url.concat(f'/devices/{id}')
    delete_response = session.delete(delete_url)
    
    # Issue warning for delete failure
    if delete_response.status_code != 200:
      warnings.warn(UserWarning(f'Deleting device with id={id} failed'))


# --------------------------------------------------------------------------------
# Verification Function
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
  