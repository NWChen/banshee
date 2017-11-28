from collections import OrderedDict
from scrapers.search_requests import Requests
from threading import Thread
from time import sleep


class Firehose(Thread):

    def __init__(self, query_interval=1, max_tweets=50):
        Thread.__init__(self)
        self.scraper = Requests()

        # queue of tweets to be pushed to the frontend
        self.queue = OrderedDict()
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
        self.options.clear()
        for option in options.keys():
            if options[option] != '':
                self.options[option] = options[option]

    '''
    Get most recent tweets.
    '''
    def get_tweets(self, num_tweets=10):
        data = list(self.queue.values())
        data = data [:num_tweets]
        print(data)
        return data

    '''
    Run this thread.
    '''
    def run(self):
        while True:
            for option, value in self.options.items():
                # call the corresponding scraper function,
                # passing in the corresponding user-defined parameters
                new_data = self.scraper_funcs[option](value)
                new_data_ids = [self.hash_tweet(tweet) for tweet in new_data]
                self.queue.update(zip(new_data_ids, new_data))
            print('FETCHED %d TWEETS' % len(self.queue.keys()))
            # trim the queue to prevent overflow
            while len(self.queue.keys()) > self.max_tweets:
                self.queue.popitem(last=False)
            sleep(self.query_interval)
