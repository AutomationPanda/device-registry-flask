"""
This module provides fixtures for integration tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest
import requests
import time
import warnings


# --------------------------------------------------------------------------------
# Class: BaseUrl
# --------------------------------------------------------------------------------

class BaseUrl:
  
  def __init__(self, base_url):
    self.base_url = base_url
  
  def concat(self, resource):
    return self.base_url + resource


# --------------------------------------------------------------------------------
# Class: User
# --------------------------------------------------------------------------------

class User:

  def __init__(self, username, password):
    self.username = username
    self.password = password


# --------------------------------------------------------------------------------
# Class: TokenHolder
# --------------------------------------------------------------------------------

class TokenHolder:

  def __init__(self, token, start_time):
    self.token = token
    self.start_time = start_time


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(test_config, index):
  users = test_config['users']
  user = User(users[index]['username'], users[index]['password'])
  return user


# --------------------------------------------------------------------------------
# Config Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_config():
  with open('tests/integration/config.json') as config_json:
    data = json.load(config_json)
  return data


@pytest.fixture
def base_url(test_config):
  return BaseUrl(test_config['base_url'])


@pytest.fixture
def user1(test_config):
  return _build_user(test_config, 0)


@pytest.fixture
def user2(test_config):
  return _build_user(test_config, 1)


# --------------------------------------------------------------------------------
# Session Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def user1_session(base_url, user1):
  session = requests.Session()
  session.auth = (user1.username, user1.password)
  return session


@pytest.fixture
def user2_session(base_url, user2):
  session = requests.Session()
  session.auth = (user2.username, user2.password)
  return session


# --------------------------------------------------------------------------------
# Token Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def user1_token(base_url, user1):
  url = base_url.concat('/authenticate/')
  auth = (user1.username, user1.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'token' in data
  return data['token']


@pytest.fixture(scope='session')
def token_holder():
  return TokenHolder(None, None)


@pytest.fixture
def user1_token_shared(test_config, token_holder):
  current_time = time.time()

  if not token_holder.token or current_time - token_holder.start_time >= 3600:    
    base_url = BaseUrl(test_config['base_url'])
    user1 = _build_user(test_config, 0)

    url = base_url.concat('/authenticate/')
    auth = (user1.username, user1.password)
    response = requests.get(url, auth=auth)
    data = response.json()

    assert response.status_code == 200
    assert 'token' in data
    
    token_holder.token = data['token']
    token_holder.start_time = current_time
  
  return token_holder.token

# --------------------------------------------------------------------------------
# Device Fixtures
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


@pytest.fixture
def light_data():
  return {
    'name': 'Front Porch Light',
    'location': 'Front Porch',
    'type': 'Light Switch',
    'model': 'GenLight 64B',
    'serial_number': 'GL64B-99987'
  }
