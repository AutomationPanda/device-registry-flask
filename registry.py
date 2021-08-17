import click
import flask
import os

from app import create_app, db
from app.models import Device


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command('init-db')
def init_db():
    """Initializes the database with devices."""

    db.drop_all()
    db.create_all()

    light = Device(
      name='Front Porch Light',
      location='Front Porch',
      type='Light Switch',
      model='GenLight 64B',
      serial_number='GL64B-99987')

    thermostat = Device(
      name='Main Thermostat',
      location='Living Room',
      type='Thermostat',
      model='ThermoBest 3G',
      serial_number='TB3G-12345')
    
    fridge = Device(
      name='Family Fridge',
      location='Kitchen',
      type='Refrigerator',
      model='El Gee Mondo21',
      serial_number='LGM-20201')

    db.session.add(light)
    db.session.add(thermostat)
    db.session.add(fridge)
    db.session.commit()
    
    click.echo('Initialized the database with fresh data.')
