"""
This module provides documentation using `flask-autodoc`.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from flask import Blueprint, jsonify
from flask_selfdoc import Autodoc


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

docs = Blueprint('doc', __name__)
auto = Autodoc()


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@docs.route('/docs/')
@auto.doc()
def docs_get():
  """
  Provides HTML documentation for the Device Registry Service REST API.
  """
  
  return auto.html(title='Device Registry Service REST API Documentation')


@docs.route('/docs/json/', methods=['GET'])
@auto.doc()
def docs_json_get():
  """
  Provides JSON documentation for the Device Registry Service REST API.
  """
  
  doc_data = auto.generate()
  for d in doc_data:
    d['args'] = list(d['args'])
  return jsonify(doc_data)
