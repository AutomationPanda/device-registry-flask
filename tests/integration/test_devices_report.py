"""
This module contains tests for device reports.
It shows how to test file downloads via REST API.
"""

# --------------------------------------------------------------------------------
# Download Tests
# --------------------------------------------------------------------------------

def test_device_report_download(base_url, session, thermostat):

  # Download
  device_id_url = base_url.concat(f'/devices/{thermostat["id"]}/report')
  get_response = session.get(device_id_url)

  # Verify response
  assert get_response.status_code == 200
  assert 'text/plain' in get_response.headers['Content-Type']
  assert int(get_response.headers['Content-Length']) > 0
  assert get_response.headers['Content-Disposition'] == 'attachment; filename="Main Thermostat.txt"'

  # Verify content
  expected_report = \
    f"ID: {thermostat['id']}\n" + \
    f"Name: {thermostat['name']}\n" + \
    f"Location: {thermostat['location']}\n" + \
    f"Type: {thermostat['type']}\n" + \
    f"Model: {thermostat['model']}\n" + \
    f"Serial Number: {thermostat['serial_number']}\n" + \
    f"Owner: {thermostat['owner']}\n"
  
  assert get_response.text == expected_report
