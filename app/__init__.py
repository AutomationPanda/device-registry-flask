"""
This module provides the app factory method.
It adds all the blueprints to the app.
This module also provides a reference to the database object and the start time.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os
import time

from config import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as JWS


# --------------------------------------------------------------------------------
# Variables
# --------------------------------------------------------------------------------

START_TIME = time.time()

db = SQLAlchemy()


# --------------------------------------------------------------------------------
# App Factory
# --------------------------------------------------------------------------------

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  db.init_app(app)
  with app.app_context():
    db.create_all()

  from .errors import errors as error_blueprint
  app.register_blueprint(error_blueprint)

  from .status import status as status_blueprint
  app.register_blueprint(status_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .devices import devices as devices_blueprint
  app.register_blueprint(devices_blueprint)

  app.jws = JWS(app.config['SECRET_KEY'], expires_in=3600)

  return app
