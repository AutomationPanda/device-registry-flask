"""
This module provides app configurations as classes.
Each config sets Flask settings like SECRET_KEY.
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

    'default': DevelopmentConfig
}