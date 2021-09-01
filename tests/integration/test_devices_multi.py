"""
This module contains integration tests for the '/devices/' resource.
These tests cover GET responses involving multiple devices.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Authentication Tests
# --------------------------------------------------------------------------------

# def test_devices_get_empty(base_url, user1_session):
#   url = base_url.concat('/devices/')
#   response = user1_session.get(url)
#   data = response.json()

#   assert response.status_code == 200
#   assert 'devices' in data


# We cannot guarantee that the devices we create are the only devices in the system.
# Create new test data in this file to prevent global changes from breaking these tests.

# Create and get exactly 3, but describe warning about parallel testing
# Create multiple and get
# Create multiple, delete, and get

# Create with unique values and get with query params
# Unsupported query params ignored
# Multiple query params
