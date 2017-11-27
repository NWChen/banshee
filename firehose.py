from collections import OrderedDict
from scrapers.search_requests import Requests
from threading import Thread
from time import sleep

class Firehose(Thread):

    def __init__(self, query_interval=1, max_tweets=10):
        Thread.__init__(self)
        self.scraper = Requests()

        self.queue = OrderedDict() # queue of tweets to be pushed to the frontend
        self.query_interval = query_interval # time, in seconds, to wait between querying the scraper
        self.max_tweets = max_tweets

        self.options = {} # query types, e.g. username, location, ...
        self.scraper_funcs = {'username': self.scraper.search_user, 'nearest_location': self.scraper.search_location, 'any_words': self.scraper.search_partial_keywords, 'all_words': self.scraper.search_exact_keywords, 'exact_phrase': self.scraper.search_exact_phrase} # pairs query types with corresponding scraper functions
                    
    '''
    Hash a tweet using its tweet id.
    '''
    def hash_tweet(self, tweet: dict):
        id = tweet['url']
        tweet['id'] = id[id.rfind('/')+1:]
        return tweet['id']

    '''
    Process incoming parameters for scraping.
    '''
    def set_options(self, options: dict):
        self.options.clear()
        for option in options.keys():
            if options[option] != '':
                self.options[option] = options[option]

    '''
    Get most recent tweets.
    '''
    def get_tweets(self):
        data = list(self.queue.values())
        data.reverse() # move most recent tweets to the top (index 0) of the list
        print(data)
        return data

    '''
    Run this thread.
    '''
    def run(self):
        while True:
            for option, value in self.options.items():
                new_data = self.scraper_funcs[option](value) # call the corresponding scraper function, passing in the corresponding user-defined parameters
                new_data_ids = [self.hash_tweet(tweet) for tweet in new_data]
                self.queue.update(zip(new_data_ids, new_data))
            print('FETCHED %d TWEETS' % len(self.queue.keys()))
            while len(self.queue.keys()) > self.max_tweets: # trim the queue to prevent overflow
                self.queue.popitem(last=False)
            sleep(self.query_interval)
