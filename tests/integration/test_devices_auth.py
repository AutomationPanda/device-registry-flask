"""
This module contains integration tests for authentication.
It uses the '/devices/' resource.
For complete testing, every endpoint should have authentication tests.
However, that would generate a lot of test cases.
In a risk-based approach, it might be better to cover only a few endpoints.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Authentication Tests
# --------------------------------------------------------------------------------

def test_devices_get_with_no_auth(base_url):
  url = base_url.concat('/devices/')
  response = requests.get(url)
  data = response.json()

  assert response.status_code == 401
  assert data['error'] == 'unauthorized'
  assert data['message'] == 'Invalid credentials'


def test_devices_get_with_basic_auth(base_url, user):
  url = base_url.concat('/devices/')
  auth = (user.username, user.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data


def test_devices_get_with_token_auth(base_url, auth_token):
  url = base_url.concat('/devices/')
  headers = {'Authorization': 'Bearer ' + auth_token}
  response = requests.get(url, headers=headers)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data


def test_devices_get_with_shared_token_auth(base_url, shared_auth_token):
  url = base_url.concat('/devices/')
  headers = {'Authorization': 'Bearer ' + shared_auth_token}
  response = requests.get(url, headers=headers)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data


# --------------------------------------------------------------------------------
# Authorization Tests
# --------------------------------------------------------------------------------

# One user cannot access another user's devices
#   * GET /devices/
#   * GET /devices/<id>
#   * PATCH /devices/<id>
#   * PUT /devices/<id>
#   * DELETE /devices/<id>
