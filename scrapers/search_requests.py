import os

from selenium import webdriver

from scrapers.tweet_searcher import TweetSearcher


class Requests(object):

    def __init__(self):
        """
        Initializes a consistent browser throughout the api calls 
        """
        chrome_path = '%s' % os.path.dirname(os.path.realpath(__file__))
        os.environ['PATH'] += ':%s' % chrome_path
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=options)

    def __del__(self):
        """
        closes the browser on the termination of the program
        """
        self.browser.close()

    def search_user(self, user_handler:str, scrolls=1):
        """
        Searches a particular user handle and returns its latest tweets
        user_handler should not contain '@'
        scrolls decided number of tweets returned
        """
        if not user_handler:
            return None
        elif user_handler[0] == '@':
            user_handler = user_handler[1:]
            
        base_url = '?f=tweets&vertical=default&q=from%3A{}'.format(user_handler)

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)

    def search_location(self, location:str, mile_radius=15, scrolls=1):
        """
        Searches all tweets around a certain mile radius
        defaults to 15 miles
        """
        if not location:
            return None
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None

        base_url = '?f=tweets&vertical=default&q=near%3A"{}"%20within%3A{}mi'.format(location, mile_radius)

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)

    def search_exact_keywords(self, keywords:list, scrolls=1):
        """
        Searches all tweets with the list of keywords
        All of the keywords must exist in the search. Treated as an "and"
        """
        if not keywords:
            return None

        base_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            base_url += '{}%20'.format(keyword)
        base_url = base_url[:len(base_url)-3]

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)

    def search_partial_keywords(self, keywords:list, scrolls=1):
        """
        Searches all tweets with the list of keywords
        Any of the keywords will yield results. Treated as an "or"
        """
        if not keywords:
            return None

        base_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            base_url += '{}%20OR%20'.format(keyword)
        base_url = base_url[:len(base_url)-8]

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)

    def search_exact_phrase(self, phrase:str, scrolls=1):
        """
        Searches all tweets with the exact phrase
        """
        if not phrase:
            return None

        base_url = '?f=tweets&vertical=default&q="'
        words = phrase.split(' ')
        for word in words:
            base_url += '{}%20'.format(word)
        base_url = base_url[:len(base_url)-3]
        base_url += '"'

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)

    def search_exact_keywords_by_location(self, keywords:list, location:str,
            mile_radius=15, scrolls=1):
        """
        runs a search where all keywords must be included near a certain location
        with a mile radius around it
        """
        if not location:
            return None
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None
        if not keywords:
            return None

        base_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            base_url += '{}%20'.format(keyword)

        base_url += 'near%3A"{}"%20within%3A{}mi'.format(location,mile_radius)

        search = TweetSearcher(self.browser, base_url)
        return search.get_tweets(scrolls)
