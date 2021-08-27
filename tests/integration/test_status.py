"""
This module contains integration tests for the '/status/' resource.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_status_get(base_url):
  url = base_url.concat('/status/')
  response = requests.get(url)
  data = response.json()
  
  assert response.status_code == 200
  assert data['online'] == True
  assert data['uptime'] > 0
  