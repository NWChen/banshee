from datetime import date, datetime
from flask import Flask, jsonify, request, Response, send_file, send_from_directory
from flask_socketio import SocketIO
from firehose import Firehose
from scrapers.search_requests import Requests as Scraper
from time import sleep

import json
import os

'''
Configure Flask app.
'''
app = Flask(__name__, static_url_path='')
firehose = Firehose()
firehose.start()
socketio = SocketIO(app)

'''
Confirm socket connection to the client.
'''
@socketio.on('connect', namespace='/stream')
def client_connect():
    print('Connected to /stream')

'''
Listen to and process inputs.
'''
@socketio.on('inputs', namespace='/stream')
def handle_inputs(data):
    firehose.set_options(data)

'''
Stream outputs to the client.
'''
@socketio.on('more', namespace='/stream')
def more_data():
    tweets = firehose.queue
    socketio.emit('data', {'data': tweets}, namespace='/stream')

'''
Serve homepage and related assets.
'''
@app.route('/')
def root():
    return send_file('index.html')

@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('css', path)

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
