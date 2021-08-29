"""
This module contains integration tests for the '/devices/' resource.
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


def test_devices_get_empty_with_basic_auth(base_url, user1):
  url = base_url.concat('/devices/')
  auth = (user1.username, user1.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data
  assert len(data['devices']) == 0


def test_devices_get_empty_with_token_auth(base_url, user1_token):
  url = base_url.concat('/devices/')
  headers = {'Authorization': 'Bearer ' + user1_token}
  response = requests.get(url, headers=headers)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data
  assert len(data['devices']) == 0


def test_devices_get_empty_with_shared_token_auth(base_url, user1_token_shared):
  url = base_url.concat('/devices/')
  headers = {'Authorization': 'Bearer ' + user1_token_shared}
  response = requests.get(url, headers=headers)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data
  assert len(data['devices']) == 0