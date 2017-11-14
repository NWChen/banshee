from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from scrapers.twitter_requests import Scrape
import os

app = Flask(__name__)
scraper = Scrape()
socketio = SocketIO(app)
thread = Thread()
thread_stop_event = Event()

@socketio.on('client_connected')
def client_connected(data):
    print('client connected with message: ' + data)

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
    socketio.run(app)
    #app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
