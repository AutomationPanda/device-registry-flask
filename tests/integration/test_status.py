"""
This module contains integration tests for the '/status/' resource.
The main method for '/status/' is GET.
Flask also automatically adds HEAD and OPTIONS responses for GET routes.
Unsupported methods should return 405 status codes.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Tests for GET
# --------------------------------------------------------------------------------

def test_status_get(base_url):
  url = base_url.concat('/status/')
  response = requests.get(url)
  data = response.json()
  
  assert response.status_code == 200
  assert data['online'] == True
  assert data['uptime'] > 0


# --------------------------------------------------------------------------------
# Tests for HEAD
# --------------------------------------------------------------------------------

def test_status_head(base_url):

  # Call HEAD
  url = base_url.concat('/status/')
  response = requests.head(url)
  
  # Response should be successful without a body
  assert response.status_code == 200
  assert response.text == ''

  # Response headers should match GET responses
  get_response = requests.get(url)
  assert len(response.headers) == len(get_response.headers)
  for header in response.headers:
    assert header in get_response.headers
    if header != 'Date' and header != 'Content-Length':
      assert response.headers[header] == get_response.headers[header]


# --------------------------------------------------------------------------------
# Tests for OPTIONS
# --------------------------------------------------------------------------------

def test_status_options(base_url):

  # Call OPTIONS
  url = base_url.concat('/status/')
  response = requests.options(url)
  
  # Response should be successful without a body
  assert response.status_code == 200
  assert response.text == ''

  # Response 'Allow' header should list supported methods
  for valid_method in ['HEAD', 'OPTIONS', 'GET']:
    assert valid_method in response.headers['Allow']


# --------------------------------------------------------------------------------
# Tests for Unsupported Methods
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
  'method, supported',
  [
    ('DELETE', ['HEAD', 'OPTIONS', 'GET']),
    ('PATCH',  ['HEAD', 'OPTIONS', 'GET']),
    ('POST',   ['HEAD', 'OPTIONS', 'GET']),
    ('PUT',    ['HEAD', 'OPTIONS', 'GET'])
  ]
)
def test_status_invalid_method(base_url, method, supported):

  # Call the unsupported method
  url = base_url.concat('/status/')
  response = requests.request(method, url)
  data = response.json()

  # Response should be a 405 error
  assert response.status_code == 405
  assert data['error'] == 'method not allowed'

  # Response should list supported methods
  for valid_method in supported:
    assert valid_method in data['valid_methods']
