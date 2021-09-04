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

from testlib.api import BaseUrl, User, TokenHolder
from testlib.devices import create_device, delete_device, verify_device_data


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(test_config, index):
  users = test_config['users']
  user = User(users[index]['username'], users[index]['password'])
  return user


def _build_session(user):
  session = requests.Session()
  session.auth = (user.username, user.password)
  return session


# --------------------------------------------------------------------------------
# Config Fixture
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
def user(test_config, user_index=0):
  return _build_user(test_config, user_index)


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
def session(user):
  return _build_session(user)


@pytest.fixture
def user1_session(user1):
  return _build_session(user1)


@pytest.fixture
def user2_session(user2):
  return _build_session(user2)


# --------------------------------------------------------------------------------
# Token Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def auth_token(base_url, user):
  url = base_url.concat('/authenticate/')
  auth = (user.username, user.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'token' in data

  return data['token']


@pytest.fixture(scope='session')
def token_holder():
  return TokenHolder(None, None)


@pytest.fixture
def shared_auth_token(base_url, user, token_holder):
  current_time = time.time()

  if not token_holder.token or current_time - token_holder.start_time >= 3600:
    url = base_url.concat('/authenticate/')
    auth = (user.username, user.password)
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
def light_data():
  return {
    'name': 'Front Porch Light',
    'location': 'Front Porch',
    'type': 'Light Switch',
    'model': 'GenLight 64B',
    'serial_number': 'GL64B-99987'
  }


@pytest.fixture
def thermostat(base_url, user, session, thermostat_data):
  device_data = create_device(base_url, user, session, thermostat_data)
  yield device_data

  if 'id' in device_data:
    delete_device(base_url, session, device_data['id'])
