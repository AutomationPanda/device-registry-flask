"""
This module provides a blueprint for status-related resources.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from . import START_TIME
from flask import Blueprint, jsonify, redirect


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

status = Blueprint('status', __name__)


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@status.route('/')
def index():
  """
  Redirects to '/status/'.
  """

  return redirect('/status/')


@status.route('/status/', methods=['GET'])
def status_get():
  """
  Provides uptime information about the web service.
  """
  
  response = {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }
  return jsonify(response)