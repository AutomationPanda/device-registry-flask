"""
This module contains CRUD integration tests for devices.
CRUD = Create, Retrieve, Update, Delete.
Positive and negative cases are included.
Thorough CRUD tests require more than one call per test.
Therefore, their names do not mirror resource paths.
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
def thermostat_patch_data():
  return {
    'name': 'Upstairs Thermostat',
    'location': 'Master Bedroom'
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


def test_create_with_no_body_yields_error(base_url, user1_session):

  # Attempt create
  device_url = base_url.concat('/devices/')
  post_response = user1_session.post(device_url)
  post_data = post_response.json()
  
  # Verify error
  assert post_response.status_code == 400
  post_data['error'] == 'bad request'
  post_data['message'] == 'The request body is missing all fields'


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
  assert post_data['error'] == 'bad request'
  assert post_data['message'] == f'The request body has invalid fields: {field}'


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
  assert post_data['error'] == 'bad request'
  assert post_data['message'] == f'The request body has missing fields: {field}'


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


def test_update_device_via_put_with_no_body_yields_error(base_url, user1_session, thermostat):

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 400
  put_data['error'] == 'bad request'
  put_data['message'] == 'The request body is missing all fields'


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

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 400
  assert put_data['error'] == 'bad request'
  assert put_data['message'] == f'The request body has invalid fields: {field}'


@pytest.mark.parametrize(
  'field',
  ['name', 'location', 'type', 'model', 'serial_number']
)
def test_update_device_via_put_with_missing_field_yields_error(
  field, base_url, user1_session, thermostat, light_data):
  del light_data[field]

  # Attempt put
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  put_response = user1_session.put(device_url, json=light_data)
  put_data = put_response.json()

  # Verify error
  assert put_response.status_code == 400
  assert put_data['error'] == 'bad request'
  assert put_data['message'] == f'The request body has missing fields: {field}'


# --------------------------------------------------------------------------------
# Update Tests for PATCH
# --------------------------------------------------------------------------------

def test_update_device_via_patch(
  base_url, user1, user1_session, thermostat, thermostat_patch_data):

  # Patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = user1_session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify patch
  assert patch_response.status_code == 200
  thermostat_patch_data['id'] = thermostat['id']
  thermostat_patch_data['type'] = thermostat['type']
  thermostat_patch_data['model'] = thermostat['model']
  thermostat_patch_data['serial_number'] = thermostat['serial_number']
  thermostat_patch_data['owner'] = user1.username
  verify_device(patch_data, thermostat_patch_data)

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{patch_data["id"]}')
  get_response = user1_session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  verify_device(get_data, patch_data)


@pytest.mark.parametrize(
  'field, value',
  [
    ('name', 'My Favorite Thermostat'),
    ('location', 'My House')
  ]
)
def test_update_device_via_patch_with_one_field(
  field, value, base_url, user1_session, user1, thermostat, thermostat_data):

  # Patch
  request_data = {field: value}
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = user1_session.patch(device_url, json=request_data)
  patch_data = patch_response.json()

  # Verify patch
  assert patch_response.status_code == 200
  thermostat_data[field] = value
  verify_device(patch_data, thermostat_data)

  # Retrieve
  device_id_url = base_url.concat(f'/devices/{patch_data["id"]}')
  get_response = user1_session.get(device_id_url)
  get_data = get_response.json()

  # Verify retrieve
  assert get_response.status_code == 200
  verify_device(get_data, patch_data)


def test_update_device_via_patch_with_no_body_yields_error(
  base_url, user1_session, thermostat):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = user1_session.patch(device_url)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 400
  patch_data['error'] == 'bad request'
  patch_data['message'] == 'The request body is missing all fields'


def test_update_nonexistent_device_via_patch_yields_error(
  base_url, user1_session, thermostat_patch_data):

  # Attempt patch
  device_url = base_url.concat(f'/devices/{NONEXISTENT_ID}')
  patch_response = user1_session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 404
  assert patch_data['error'] == 'not found'


@pytest.mark.parametrize(
  'field, value',
  [
    ('id', EXPLICIT_ID),
    ('owner', 'nobody'),
    ('type', 'Light Switch'),
    ('model', 'ABC123'),
    ('serial_number', 'ABC123'),
    ('garbage', 'nonsense')
  ]
)
def test_update_device_via_patch_with_invalid_field_yields_error(
  field, value, base_url, user1_session, thermostat, thermostat_patch_data):
  thermostat_patch_data[field] = value

  # Attempt patch
  device_url = base_url.concat(f'/devices/{thermostat["id"]}')
  patch_response = user1_session.patch(device_url, json=thermostat_patch_data)
  patch_data = patch_response.json()

  # Verify error
  assert patch_response.status_code == 400
  assert patch_data['error'] == 'bad request'
  assert patch_data['message'] == f'The request body has invalid fields: {field}'


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
