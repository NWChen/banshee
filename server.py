from datetime import date, datetime
from flask import Flask, jsonify, request, Response, send_file, send_from_directory
from flask_socketio import SocketIO
from scrapers.search_requests import Requests as Scraper
from time import sleep

import json
import os

app = Flask(__name__, static_url_path='')
scraper = Scraper()
socketio = SocketIO(app)

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
    # this seen set (cache) should be outside the streaming loop
    seen_tweets = set()
    username = data['username']
    exact_phrase = data['exact_phrase'] #TODO: change fields to the new form inputs
    tweets = []
    if exact_phrase:
        data = scraper.search_exact_phrase(exact_phrase)
        tweets.extend(data)
    if username:
        data = scraper.search_user(username) #TODO: clean this up
        print(data)
        tweets.extend(data)
    # this can be the implementation of the caching
    '''
    filtered = []
    for tweet in tweets:
        if tweet['url'] not in seen_tweets:
            filtered.append(tweet)
            seen_tweets.add(tweet['url'])
    tweets = filtered
    '''
    # optional- to create two cache sets, one for last batch, one for current batch
    # then replace last = current at the end of the loop
    # this would be because no more than 40 tweets will arrive from each request
    # so no need to remember further back than the last batch or two

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
