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

@socketio.on('connect', namespace='/stream')
def client_connect():
    print('CONNECTED')

@socketio.on('inputs', namespace='/stream')
def handle_inputs(data):
    keywords = data['keywords'].split(' ')
    tweets = scraper.get_by_keywords(keywords)
    tweets = json.dumps(json_serial(tweets))
    socketio.emit('tweets', {'tweets': tweets}, namespace='/stream')
    print('emitted')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    username = request.form['username']
    earliest_date = request.form['earliest-date']
    latest_date = request.form['latest-date']
    keywords = request.form['keywords']
    retweets = request.form['retweets']
    tweets = ''
    if keywords:
        tweets = scraper.get_by_keywords(keywords.split(','))
    elif username:
        tweets = scraper.get_by_username(username)
    tweets = str(tweets)
    return render_template('index.html', data=tweets)

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
    #app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
