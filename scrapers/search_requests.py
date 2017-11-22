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

    def _run_on_url(self, query_url, scrolls):
        """
        runs the tweet scraper on the given url
        """
        search = TweetSearcher(self.browser, query_url)
        return search.get_tweets(scrolls)

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
            
        query_url = '?f=tweets&vertical=default&q=from%3A{}'.format(user_handler)

        return self._run_on_url(query_url, scrolls)

    def search_location(self, location:str, mile_radius=15, scrolls=1):
        """
        Searches all tweets around a certain mile radius
        defaults to 15 miles
        """
        if not location:
            return None
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None

        query_url = '?f=tweets&vertical=default&q=near%3A"{}"%20within%3A{}mi'.format(location, mile_radius)

        return self._run_on_url(query_url, scrolls)

    def search_exact_keywords(self, keywords:list, scrolls=1):
        """
        Searches all tweets with the list of keywords
        All of the keywords must exist in the search. Treated as an "and"
        """
        if not keywords:
            return None

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20'.format(keyword)

        query_url = query_url[:len(query_url)-3]

        return self._run_on_url(query_url, scrolls)

    def search_partial_keywords(self, keywords:list, scrolls=1):
        """
        Searches all tweets with the list of keywords
        Any of the keywords will yield results. Treated as an "or"
        """
        if not keywords:
            return None

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20OR%20'.format(keyword)
        query_url = query_url[:len(query_url)-8]

        return self._run_on_url(query_url, scrolls)

    def search_exact_phrase(self, phrase:str, scrolls=1):
        """
        Searches all tweets with the exact phrase
        """
        if not phrase:
            return None

        query_url = '?f=tweets&vertical=default&q="'
        words = phrase.split(' ')
        for word in words:
            query_url += '{}%20'.format(word)
        query_url = query_url[:len(query_url)-3]
        query_url += '"'

        return self._run_on_url(query_url, scrolls)

    def search_exact_keywords_by_location(self, keywords:list, location:str,
            mile_radius=15, scrolls=1):
        """
        runs a search where all keywords must be included near a certain location
        with a mile radius around it
        """
        if not location:
            return self.search_exact_keywords(keywords, scrolls)
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None
        if not keywords:
            return self.search_location(location, mile_radius, scrolls)

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20'.format(keyword)

        query_url += 'near%3A"{}"%20within%3A{}mi'.format(location,mile_radius)

        return self._run_on_url(query_url, scrolls)

    def search_partial_keywords_by_location(self, keywords:list, location:str,
            mile_radius=15, scrolls=1):
        """
        runs a search where any keywords can be included near a certain location
        with a certain mile radius around it
        """
        if not location:
            return self.search_partial_keywords(keywords, scrolls)
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None
        if not keywords:
            return self.search_location(location, mile_radius, scrolls)

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20OR%20'.format(keyword)
        query_url = query_url[:len(query_url)-5]

        query_url += 'near%3A"{}"%20within%3A{}mi'.format(location,mile_radius)

        return self._run_on_url(query_url, scrolls)

    def search_exact_phrase_by_location(self, phrase:str, location:str,
            mile_radius=15, scrolls=1):
        """
        runs a search where an exact phrase can be included near a certain location
        """
        if not location:
            return self.search_exact_phrase(phrase, scrolls)
        if mile_radius < 1 or not isinstance(mile_radius, int):
            return None
        if not phrase:
            return self.search_location(location, mile_radius, scrolls)

        query_url = '?f=tweets&vertical=default&q="'
        words = phrase.split(' ')
        for word in words:
            query_url += '{}%20'.format(word)
        query_url = query_url[:len(query_url)-3]
        query_url += '"%20'
        query_url += 'near%3A"{}"%20within%3A{}mi'.format(location,mile_radius)

        return self._run_on_url(query_url, scrolls)

    def search_exact_keywords_by_username(self, keywords:list, user_handler:str, scrolls=1):
        """
        Searches all tweets from @user_handler with the list of keywords
        must match all keywords
        """
        if not user_handler:
            return self.search_exact_keywords(keywords, scrolls)
        elif user_handler[0] == '@':
            user_handler = user_handler[1:]
        if not keywords:
            return self.search_user(user_handler, scrolls)

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20'.format(keyword)
        query_url += 'from%3A{}'.format(user_handler)

        return self._run_on_url(query_url, scrolls)

    def search_partial_keywords_by_username(self, keywords:list, user_handler:str, scrolls=1):
        """
        Searches all tweets from @user_handler with the list of keywords
        only one keyword need be in the tweet to be returned
        """
        if not user_handler:
            return self.search_partial_keywords(keywords, scrolls)
        elif user_handler[0] == '@':
            user_handler = user_handler[1:]
        if not keywords:
            return self.search_user(user_handler, scrolls)

        query_url = '?f=tweets&vertical=default&q='
        for keyword in keywords:
            query_url += '{}%20OR%20'.format(keyword)
        query_url = query_url[:len(query_url)-5]
        query_url += 'from%3A{}'.format(user_handler)

        return self._run_on_url(query_url, scrolls)

    def search_exact_phrase_by_username(self, phrase:str, user_handler:str, scrolls=1):
        """
        Searches all tweets from @user_handler with exact phrase specified
        """
        if not user_handler:
            return self.search_exact_phrase(phrase, scrolls)
        elif user_handler[0] == '@':
            user_handler = user_handler[1:]
        if not phrase:
            return self.search_user(user_handler, scrolls)

        query_url = '?f=tweets&vertical=default&q="'
        words = phrase.split(' ')
        for word in words:
            query_url += '{}%20'.format(word)
        query_url = query_url[:len(query_url)-3]
        query_url += '"%20'
        query_url += 'from%3A{}'.format(user_handler)

        return self._run_on_url(query_url, scrolls)
