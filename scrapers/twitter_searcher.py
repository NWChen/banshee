import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class TweetSearcher(object):

    def __init__(self, query=''):
        """
        Initializes the browser based on the query path
        example path: 'donald%20trump&src=typd&lang=en'
        """
        chrome_path = '%s' % os.path.dirname(os.path.realpath(__file__))
        os.environ['PATH'] += ':%s' % chrome_path
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        base_url = 'https://twitter.com/search'
        url = base_url + query 
        self.browser.get(url)

    def scroller(self, scrolls=1):
        """
        scrolls the given browser for a certain number of times, defined by count
        returns the browser web page data
        """
        cur = self.browser.execute_script('return document.body.scrollHeight')
        count = 0
        while count < scrolls or prev == cur:
            prev = cur
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            cur = self.browser.execute_script('return document.body.scrollHeight')
            count += 1

        data = self.browser.page_source
        self.browser.close()
        return data

    def get_tweets(self, scrolls=1):
        """
        Returns in a list dictionary formatted tweets
        Takes in an initialized browser and number of scrolls
        """
        tweets = []
        # scroll and collect the data into beautiful soup for parsing
        soup = BeautifulSoup(self.scroller(scrolls), 'html.parser')

        for t in soup.find_all('li', {'data-item-type':'tweet'}):        

            # scrape out the relevant tweet info
            username = t.find('span', {'class':'username'})
            if username is not None:
                username = username.get_text()
            else:
                username = ''
            link = 'https://twitter.com' + t.small.a['href'] if t.small is not None else ''
            date = t.small.a['title'] if t.small is not None else ''
            text = (t.p.get_text())
            stats = t.find('div', {'class': 'ProfileTweet-actionList js-actions'})
            # format the stats into a dict
            if stats is not None:
                stats = stats.get_text().replace('\n','')
                stats_formatted = {}
                i = 0
                words = ['Reply', 'Retweet', 'Retweeted', 'Like', 'Liked']
                for w in words:
                    i += len(w)
                    count = ''
                    while i < len(stats) and stats[i] != 'R' and stats[i] != 'L':
                        char = stats[i]
                        count += char
                        i += 1
                    if not count:
                        count = '0'
                    stats_formatted[w] = count
                
            tweet = {
            'url': link,
            'user': username,
            'date': date,
            'stats': stats_formatted,
            'content': text,
            }
            tweets.append(tweet)

        return tweets
