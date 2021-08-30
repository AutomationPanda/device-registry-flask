"""
This module contains CRUD integration tests for devices.
Thorough CRUD tests require more than one call per test.
Therefore, their names do not parallel resource paths.
"""

# --------------------------------------------------------------------------------
# "Constants"
# --------------------------------------------------------------------------------

EXPLICIT_ID = 500
NONEXISTENT_ID = 999999999


# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests
import warnings


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def thermostat_data():
  return {
    'name': 'Main Thermostat',
    'location': 'Living Room',
    'type': 'Thermostat',
    'model': 'ThermoBest 3G',
    'serial_number': 'TB3G-12345'
  }


@pytest.fixture
def light_data():
  return {
    'name': 'Front Porch Light',
    'location': 'Front Porch',
    'type': 'Light Switch',
    'model': 'GenLight 64B',
    'serial_number': 'GL64B-99987'
  }


@pytest.fixture
def thermostat(base_url, user1, user1_session, thermostat_data):

  # Create
  device_url = base_url.concat('/devices/')
  post_response = user1_session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify create
  assert post_response.status_code == 200
  thermostat_data['owner'] = user1.username
  verify_device(post_data, thermostat_data)

  # Return created device
  yield post_data

  # Cleanup if device still exists
  if 'id' in post_data:

    # Delete
    delete_url = base_url.concat(f'/devices/{post_data["id"]}')
    delete_response = user1_session.delete(delete_url)
    
    # Issue warning for delete failure
    if delete_response.status_code != 200:
      warnings.warn(UserWarning(f'Deleting device with id={{post_data["id"]}} failed'))


# --------------------------------------------------------------------------------
# Verification Functions
# --------------------------------------------------------------------------------

def verify_device(actual, expected):

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


# --------------------------------------------------------------------------------
# CRUD Tests
#
# CRUD: Create, Retrieve, Update, Delete.
# These tests provide a starting pattern.
# They can be used for databases, service APIs, or Web UIs.
# Always leave no trace: create new records and delete them after testing.
# Isolate each interaction.
# Mocking or behind-the-curtain calls can be done for setup.
#
# A note about deleting devices:
# If every test run has a "new" or "fresh" database,
# then deleting devices after each test is not required.
# However, if the database persists,
# then it might be worthwhile to make each test delete the devices it creates,
# in order to prevent the database from overflowing with disposable data.
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# Create Tests
# --------------------------------------------------------------------------------

def test_create_and_retrieve_device(base_url, user1_session, thermostat):

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  get_response = user1_session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  verify_device(get_data, thermostat)


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_create_with_invalid_field_yields_error(
  field, value, base_url, user1_session, thermostat_data):
  thermostat_data[field] = value

  # Attempt create
  device_url = base_url.concat('/devices/')
  post_response = user1_session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify error
  assert post_response.status_code == 400
  post_data['error'] == 'bad request'
  post_data['message'] == f'The device has invalid fields: {field}'


@pytest.mark.parametrize(
  'field',
  ['name', 'location', 'type', 'model', 'serial_number']
)
def test_create_with_missing_field_yields_error(field, base_url, user1_session, thermostat_data):
  del thermostat_data[field]

  # Attempt create
  device_url = base_url.concat('/devices/')
  post_response = user1_session.post(device_url, json=thermostat_data)
  post_data = post_response.json()
  
  # Verify error
  assert post_response.status_code == 400
  post_data['error'] == 'bad request'
  post_data['message'] == f'The device has invalid fields: {field}'


# --------------------------------------------------------------------------------
# Retrieve Tests
# --------------------------------------------------------------------------------

def test_retrieve_nonexistent_device_yields_error(base_url, user1_session):

  # Attempt retrieve
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  get_response = user1_session.get(device_url)
  get_data = get_response.json()

  # Verify error
  assert get_response.status_code == 404
  assert get_data['error'] == 'not found'


# --------------------------------------------------------------------------------
# Update Tests for PUT
# --------------------------------------------------------------------------------

def test_update_device_via_put(base_url, user1, user1_session, thermostat, light_data):

  # Put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify put
  assert put_response.status_code == 200
  light_data['id'] = thermostat['id']
  light_data['owner'] = user1.username
  verify_device(put_data, light_data)

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{light_data["id"]}')
  get_response = user1_session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  verify_device(get_data, put_data)


def test_update_nonexistent_device_via_put_yields_error(base_url, user1_session, light_data):

  # Attempt put
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 404
  assert put_data['error'] == 'not found'


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('garbage', 'nonsense')
  ]
)
def test_update_device_via_put_with_invalid_field_yields_error(
  field, value, base_url, user1_session, thermostat, light_data):
  light_data[field] = value

  # Put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify put
  assert put_response.status_code == 400
  put_data['error'] == 'bad request'
  put_data['message'] == f'The device has invalid fields: {field}'


@pytest.mark.parametrize(
  'field',
  ['name', 'location', 'type', 'model', 'serial_number']
)
def test_update_device_via_put_with_missing_field_yields_error(
  field, base_url, user1_session, thermostat, light_data):
  del light_data[field]

  # Put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify put
  assert put_response.status_code == 400
  put_data['error'] == 'bad request'
  put_data['message'] == f'The device has missing fields: {field}'


# --------------------------------------------------------------------------------
# Update Tests for PATCH
# --------------------------------------------------------------------------------

# Good PATCH
# Bad PATCH with missing fields
# Bad PATCH with invalid fields
# Bad PATCH with extra stuff
# Bad PATCH with nonexistent ID
# Bad PATCH with ID in body


# --------------------------------------------------------------------------------
# Delete Tests
# --------------------------------------------------------------------------------

def test_delete_device(base_url, user1_session, thermostat):

  # Delete
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}')
  delete_response = user1_session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify delete
  assert delete_response.status_code == 200
  assert not delete_data

  # Mark device as deleted
  del thermostat['id']


def test_delete_nonexistent_device(base_url, user1_session):

  # Delete
  device_id_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  delete_response = user1_session.delete(device_id_url)
  delete_data = delete_response.json()

  # Verify error
  assert delete_response.status_code == 404
  assert delete_data['error'] == 'not found'
