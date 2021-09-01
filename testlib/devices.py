"""
This module provides support for testing devices.
"""

# --------------------------------------------------------------------------------
# Verification Functions
# --------------------------------------------------------------------------------

def verify_device_data(actual, expected):

  # Verify ID
  if 'id' in expected:
    assert actual['id'] == expected['id']
  else:
    assert isinstance(actual['id'], int)
  
  # Verify field length
  fields = ['name', 'location', 'type', 'model', 'serial_number', 'owner']
  assert len(actual) == len(fields) + 1

  # Verify field values
  for field in fields:
    assert field in actual
    assert actual[field] == expected[field]
  