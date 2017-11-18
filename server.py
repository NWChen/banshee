from datetime import date, datetime
from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from scrapers.twitter_requests import Scrape
from threading import Event, Thread
from time import sleep

import json
import os

app = Flask(__name__)
scraper = Scrape()
socketio = SocketIO(app)
thread = Thread()
thread_stop_event = Event()

'''
Scrape Twitter for recent data at regular intervals.
'''
class DataThread(Thread):
    def __init__(self):
        self.interval = 1.0
        self.keywords = '0'
        super(DataThread, self).__init__()

    def generate_data(self):
        while not thread_stop_event.isSet():
            if self.keywords != '0':
                tweets = scraper.get_by_keywords(self.keywords.split(','))
                tweets = json.dumps(tweets, default=json_serial)
                socketio.send({'contents': tweets}, namespace='/stream')
                print('emitting data:')
                print(tweets[:10])
            sleep(self.interval)

    def run(self):
        self.generate_data()

'''
Serialize JSON objects that include datetimes.
'''
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

'''
Handle client requests and serve relevant client views.
'''
@socketio.on('connect', namespace='/stream')
def init_stream():
    global thread #TODO: make this not global
    if not thread.isAlive():
        print('STARTING THREAD')
        thread = DataThread()
        thread.start()

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
        global thread #TODO: make this not global
        thread.keywords = keywords
        #tweets = scraper.get_by_keywords(keywords.split(','))
    elif username:
        tweets = scraper.get_by_username(username)
    tweets = str(tweets)
    return render_template('index.html', data=tweets)

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
    #app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
