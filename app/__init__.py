"""
This module provides the app factory method.
It adds all the blueprints to the app.
This module also provides a reference to the database object, users, and the start time.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from config import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


# --------------------------------------------------------------------------------
# Variables
# --------------------------------------------------------------------------------

START_TIME = time.time()

db = SQLAlchemy()
users = dict()


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

  username1 = app.config['AUTH_USERNAME1']
  password1 = generate_password_hash(app.config['AUTH_PASSWORD1'])
  users[username1] = password1

  username2 = app.config['AUTH_USERNAME2']
  password2 = generate_password_hash(app.config['AUTH_PASSWORD2'])
  users[username2] = password2

  return app
