from scrapers.search_requests import Requests
from threading import Thread
from time import sleep

class Firehose(Thread):

    def __init__(self, query_interval=1):
        Thread.__init__(self)
        self.scraper = Requests()

        self.ids = set() # set of unique tweet ids
        self.queue = [] # queue of tweets to be pushed to the frontend
        self.query_interval = query_interval # time, in seconds, to wait between querying the scraper

        self.options = {} # query types, e.g. username, location, ...
        self.scraper_funcs = {'username': self.scraper.search_user, 'location': self.scraper.search_location, 'any_words': self.scraper.search_partial_keywords, 'all_words': self.scraper.search_exact_keywords, 'exact_phrase': self.scraper.search_exact_phrase} # pairs query types with corresponding scraper functions
                    
    '''
    Hash a tweet for convenient storage in `ids`.
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
    Run this thread.
    '''
    def run(self):
        while True:
            print('im gettin your shit')
            for option, value in self.options.items():
                new_data = self.scraper_funcs[option](value) # call the corresponding scraper function, passing in the corresponding user-defined parameters
                self.ids.union([self.hash_tweet(tweet) for tweet in new_data])
                self.queue.extend(new_data)
            self.queue = [tweet for tweet in self.queue if self.hash_tweet(tweet) not in self.ids] # remove duplicates from tweet queue
            # TODO: truncate queue if it exceeds a certain length
            sleep(self.query_interval)
