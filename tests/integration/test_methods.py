"""
This module contains integration tests for different request methods.
Flask automatically adds HEAD and OPTIONS responses for GET routes.
Unsupported methods should return 405 status codes.
These methods should be tested, but the tests are repetitive.
Tests should be parametrized together to minimize code duplication.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Method Tests for HEAD
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
  'resource',
  [
    ('/status/')
  ]
)
def test_head(base_url, resource):

  # Call HEAD
  url = base_url.concat(resource)
  response = requests.head(url)
  
  # Response should be successful without a body
  assert response.status_code == 200
  assert response.text == ''

  # Response headers should match GET responses
  get_response = requests.get(url)
  assert len(response.headers) == len(get_response.headers)
  for header in response.headers:
    assert header in get_response.headers
    if header != 'Date':
      assert response.headers[header] == get_response.headers[header]


# --------------------------------------------------------------------------------
# Method Tests for OPTIONS
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
  'resource, supported',
  [
    ('/status/', ['HEAD', 'OPTIONS', 'GET'])
  ]
)
def test_status_options(base_url, resource, supported):

  # Call OPTIONS
  url = base_url.concat(resource)
  response = requests.options(url)
  
  # Response should be successful without a body
  assert response.status_code == 200
  assert response.text == ''

  # Response 'Allow' header should list supported methods
  for valid_method in supported:
    assert valid_method in response.headers['Allow']


# --------------------------------------------------------------------------------
# Unsupported Method Tests
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
  'resource, method, supported',
  [
    ('/status/', 'DELETE', ['HEAD', 'OPTIONS', 'GET']),
    ('/status/', 'PATCH', ['HEAD', 'OPTIONS', 'GET']),
    ('/status/', 'POST', ['HEAD', 'OPTIONS', 'GET']),
    ('/status/', 'PUT', ['HEAD', 'OPTIONS', 'GET'])
  ]
)
def test_status_invalid_method(base_url, resource, method, supported):

  # Call the unsupported method
  url = base_url.concat(resource)
  response = requests.request(method, url)
  data = response.json()

  # Response should be a 405 error
  assert response.status_code == 405
  assert data['error'] == 'method not allowed'

  # Response should list supported methods
  for valid_method in supported:
    assert valid_method in data['valid_methods']
