import time
from flask import Flask


app = Flask(__name__)
start_time = time.time()


@app.route('/')
def index():
  return 'This is a device registry REST API.'


@app.route('/online/')
def online():
  response = {
    'online': True,
    'uptime': round(time.time() - start_time, 3)
  }
  return response


@app.route('/devices/')
def device():
  return { 'devices': ['A', 'B', 'C'] }


@app.route('/devices/<id>')
def device_id(id):
  return id


@app.route('/devices/<id>/report')
def devices_id_report(id):
  return id


@app.route('/devices/<id>/image')
def devices_id_image(id):
  return id
