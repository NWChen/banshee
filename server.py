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
Extract tweet ID from tweet URL given entire tweet object.
'''
def get_id(tweet):
    id = tweet['url']
    id = id[id.rfind('/')+1:]
    return id

'''
Listen to and process inputs. Return outputs to the client.
'''
@socketio.on('inputs', namespace='/stream')
def handle_inputs(data):
    username = data['username']
    location = data['location']
    mile_radius = data['mile_radius']
    any_words = data['any_words']
    all_words = data['all_words']
    exact_phrase = data['exact_phrase']

    # this seen set (cache) should be outside the streaming loop
    seen_tweets = set()

    tweets = []
    if username:
        data = scraper.search_user(username)
        tweets.extend(data)
    if location:
        if mile_radius:
            data = scraper.search_location(location, int(mile_radius)) #TODO: validate mile_radius as int on frontend
            tweets.extend(data)
        else:
            data = scraper.search_location(location)
            tweets.extend(data)
    if any_words:
        data = scraper.search_partial_keywords(any_words)
        tweets.extend(data)
    if all_words:
        data = scraper.search_exact_keywords(all_words)
        tweets.extend(data)
    if exact_phrase:
        data = scraper.search_exact_phrase(exact_phrase)
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

    for tweet in tweets:
        tweet['id'] = get_id(tweet)
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
