from flask import Flask, jsonify, render_template, request, Response
#from flask_socketio import SocketIO, send, emit
from scrapers.twitter_requests import Scrape

app = Flask(__name__)
scraper = Scrape()
#socketio = SocketIO(app)

#@socketio.on('client_connected')
def handle_client_connection(json):
    print('connection state: %s' % str(json))

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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
