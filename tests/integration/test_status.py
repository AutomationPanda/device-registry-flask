import pytest
import requests


class BaseUrl:
  
  def __init__(self, base_url):
    self.base_url = base_url
  
  def concat(self, resource):
    return self.base_url + resource


@pytest.fixture(scope='session')
def test_config():
  return {
    'base_url': 'http://127.0.0.1:5000'
  }


@pytest.fixture
def base_url(test_config):
  return BaseUrl(test_config['base_url'])


def test_status_get(base_url):
  url = base_url.concat('/status/')
  response = requests.get(url)
  data = response.json()
  
  assert response.status_code == 200
  assert data['online'] == True
  assert data['uptime'] > 0
  

def test_status_head(base_url):
  url = base_url.concat('/status/')
  response = requests.head(url)
  
  assert response.status_code == 200
  assert response.text == ''

  get_response = requests.get(url)
  assert len(response.headers) == len(get_response.headers)
  for header in response.headers:
    assert header in get_response.headers
    if header != 'Date':
      assert response.headers[header] == get_response.headers[header]


def test_status_options(base_url):
  url = base_url.concat('/status/')
  response = requests.options(url)
  
  assert response.status_code == 200
  assert response.text == ''

  for valid_method in ['HEAD', 'OPTIONS', 'GET']:
    assert valid_method in response.headers['Allow']


@pytest.mark.parametrize(
  'method',
  ['DELETE', 'PATCH', 'POST', 'PUT']
)
def test_status_invalid_method(base_url, method):
  url = base_url.concat('/status/')
  response = requests.request(method, url)
  data = response.json()

  assert response.status_code == 405
  assert data['error'] == 'method not allowed'

  for valid_method in ['HEAD', 'OPTIONS', 'GET']:
    assert valid_method in data['valid_methods']
