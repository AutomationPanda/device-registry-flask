"""
This module provides app configurations as classes.
Each config sets Flask settings like SECRET_KEY.
Many settings can be overridden using environment variables.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os


# --------------------------------------------------------------------------------
# Variables
# --------------------------------------------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))


# --------------------------------------------------------------------------------
# Configuration Objects
# --------------------------------------------------------------------------------

class Config:
  AUTH_PASSWORD1 = os.environ.get('AUTH_PASSWORD1') or 'I<3testing'
  AUTH_PASSWORD2 = os.environ.get('AUTH_PASSWORD2') or 'Muh5devices'
  AUTH_TOKEN_EXPIRATION = int(os.environ.get('AUTH_TOKEN_EXPIRATION') or 3600)
  AUTH_USERNAME1 = os.environ.get('AUTH_USERNAME1') or 'pythonista'
  AUTH_USERNAME2 = os.environ.get('AUTH_USERNAME2') or 'engineer'
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'Pandas are awesome!'
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'registry_data.sqlite')


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite://'


# --------------------------------------------------------------------------------
# Configuration Dictionary
# --------------------------------------------------------------------------------

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': TestingConfig
}