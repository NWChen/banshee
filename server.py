from datetime import date, datetime
from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from scrapers.search_requests import Requests as Scraper
from time import sleep

import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

'''
Serialize JSON objects that include datetimes
'''
def serial_json(list_of_objs):
    for objs in list_of_objs:
        for key in objs.keys():
            if isinstance(objs[key], (datetime, date)):
                objs[key] = objs[key].isoformat()
    return objs

'''
Generate formatted JSON based on included tokens.
#TODO - delete this?
'''
def format_json(tweet:dict, keyword=''):
    data = {}
    content = tweet['content']
    return json.dumps(data)

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
    username = data['username']
    exact_phrase = data['exact_phrase'] #TODO: change fields to the new form inputs
    tweets = []
    scraper = Scraper()
    if exact_phrase:
        tweets.extend(scraper.search_exact_phrase(exact_phrase))
    if username:
        temp = scraper.search_user(username) #TODO: clean this up
        tweets.extend(temp)
    tweets = json.dumps(serial_json(tweets))

    keywords = exact_phrase #TODO: adapt this for other fields too
    print(tweets, keywords)
    socketio.emit('data', {'data': tweets, 'keywords': keywords}, namespace='/stream')

'''
Serve homepage.
'''
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
