"""
This module provides a blueprint for status-related resources.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from . import START_TIME
from flask import Blueprint, jsonify


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

status = Blueprint('status', __name__)


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@status.route('/')
def index():
  return 'This is a device registry REST API.'


@status.route('/status/', methods=['GET'])
def get_status():
  response = {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }
  return jsonify(response)