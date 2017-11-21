from datetime import date, datetime
from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from scrapers.twitter_requests import Scrape
from time import sleep

import json
import os

app = Flask(__name__)
scraper = Scrape()
socketio = SocketIO(app)

'''
Serialize JSON objects that include datetimes.
'''
def json_serial(list_of_objs):
    for objs in list_of_objs: #TODO: make this more efficient
        for key in objs.keys():
            if isinstance(objs[key], (datetime, date)):
                objs[key] = objs[key].isoformat()
    return objs

'''
Confirm socket connection to the client.
'''
@socketio.on('connect', namespace='/stream')
def client_connect():
    print('Connected to /stream')

'''
Listen to and process inputs. Return outputs to the client.
'''
@socketio.on('inputs', namespace='/stream')
def handle_inputs(data):
    keywords = data['keywords'].split(' ')
    tweets = scraper.get_by_keywords(keywords)
    tweets = json.dumps(json_serial(tweets))
    socketio.emit('tweets', {'tweets': tweets}, namespace='/stream')

'''
Serve homepage.
'''
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
