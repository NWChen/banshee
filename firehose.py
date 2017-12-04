from collections import defaultdict
from scrapers.search_requests import Requests
from threading import Thread
from time import sleep


class Firehose(Thread):

    def __init__(self, query_interval=1, max_tweets=50):
        Thread.__init__(self)
        self.scraper = Requests()

        # queue of tweets to be pushed to the frontend
        self.queue = []
        # time, in seconds, to wait between querying the scraper
        self.query_interval = query_interval
        self.max_tweets = max_tweets

        # query types, e.g. username, location, ...
        self.options = {}
        # pairs query types with corresponding scraper functions
        self.scraper_funcs = {'username': self.scraper.search_user, 
            'nearest_location': self.scraper.search_location, 
            'any_words': self.scraper.search_partial_keywords, 
            'all_words': self.scraper.search_exact_keywords, 
            'exact_phrase': self.scraper.search_exact_phrase}
                    
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
        del self.queue[:] # clear queue
        self.options.clear()
        for option in options.keys():
            if options[option] != '':
                self.options[option] = options[option]

    '''
    Get most recent tweets.
    '''
    def get_tweets(self, num_tweets=10):
        #return self.queue[:num_tweets]
        tweet = self.queue[-1:]
        del self.queue[-1:]
        return tweet

    '''
    Remove duplicate tweets (dictionaries) in a list. 
    Duplicate tweets share the same id.
    '''
    def unduplicate(self, ls=list):
        ids = [self.hash_tweet(tweet) for tweet in ls]
        ids_count = defaultdict(int)
        for id in ids:
            ids_count[id] += 1
        for i, tweet in enumerate(ls):
            id = self.hash_tweet(tweet)
            if ids_count[id] > 1:
                del ls[i]
                ids_count[id] -= 1
        return ls

    '''
    Run this thread.
    '''
    def run(self):
        while True:
            try:
                for option, value in self.options.items():
                    # call the corresponding scraper function,
                    # passing in the corresponding user-defined parameters
                    data = self.scraper_funcs[option](value)
                    self.queue = data + self.queue # append to front of queue
                    self.queue = self.unduplicate(self.queue)
                print('FETCHED %d TWEETS' % len(self.queue))
                del self.queue[self.max_tweets:] # pop old elements
            except RuntimeError: # new options (queries) submitted from user
                pass 
            sleep(self.query_interval)
