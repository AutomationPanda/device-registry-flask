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

    device = Device(
      name='Main Thermostat',
      location='Living Room',
      type='Thermostat',
      model='ThermoBest 3G',
      serial_number='TB3G-12345')
    
    db.session.add(device)
    db.session.commit()
    
    click.echo('Initialized the database with fresh data.')
