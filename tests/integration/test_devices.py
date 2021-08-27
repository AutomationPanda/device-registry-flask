"""
This module contains integration tests for the '/devices/' resource.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_devices_get_noauth(base_url):
  url = base_url.concat('/devices/')
  response = requests.get(url)
  data = response.json()

  assert response.status_code == 401
  assert data['error'] == 'unauthorized'
  assert data['message'] == 'Invalid credentials'


def test_devices_get_empty(base_url, user1):
  url = base_url.concat('/devices/')
  auth = (user1.username, user1.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'devices' in data
  assert len(data['devices']) == 0
