"""
This module contains integration tests for the '/devices/' resource.
These tests cover GET responses involving multiple devices.
We cannot guarantee that the devices we create will be the only devices in the system.
For example, if tests run in parallel, then other tests might create new devices.
Therefore, test assertions must check only what is covered by the test.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import requests


# --------------------------------------------------------------------------------
# Tests for Multiple Devices
# --------------------------------------------------------------------------------

# def test_multiple_device_creation_universally(base_url, session):
#   url = base_url.concat('/devices/')
#   response = session.get(url)
#   data = response.json()

#   assert response.status_code == 200
#   assert 'devices' in data


# Create new test data in this file to prevent global changes from breaking these tests.

# Create and get exactly 3, but describe warning about parallel testing
# Create multiple and get
# Create multiple, delete, and get

# Create with unique values and get with query params
# Unsupported query params ignored
# Multiple query params
