"""
This module provides fixtures for integration tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest


# --------------------------------------------------------------------------------
# Class: BaseUrl
# --------------------------------------------------------------------------------

class BaseUrl:
  
  def __init__(self, base_url):
    self.base_url = base_url
  
  def concat(self, resource):
    return self.base_url + resource


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_config():
  with open('tests/integration/config.json') as config_json:
    data = json.load(config_json)
  return data


@pytest.fixture
def base_url(test_config):
  return BaseUrl(test_config['base_url'])
