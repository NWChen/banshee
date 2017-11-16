from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from scrapers.twitter_requests import Scrape
from threading import Event, Thread

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
        self.keywords = ''
        super(DataThread, self).__init__()

    def generate_data(self):
        while not thread_stop_event.isSet():
            tweets = scraper.get_by_keywords(self.keywords.split(','))
            tweets = json.dumps(tweets)
            print(tweets)
            socketio.emit('data', {'contents': tweets}, namespace='/data')
            sleep(self.interval)

    def run(self):
        self.generate_data()

'''
Handle client requests and serve relevant client views.
'''
@socketio.on('client_connected')
def client_connected(data):
    print('client connected with message: ' + data)
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
        tweets = scraper.get_by_keywords(keywords.split(','))
    elif username:
        tweets = scraper.get_by_username(username)
    tweets = str(tweets)
    return render_template('index.html', data=tweets)

if __name__ == '__main__':
    print('APP STARTED')
    socketio.run(app)
    #app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
