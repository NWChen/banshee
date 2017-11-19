import time

from bs4 import BeautifulSoup
from selenium import webdriver


class TweetSearcher(object):

	def __init__(self, query=''):
		"""
		Initializes the browser based on the query path
		example path: 'donald%20trump&src=typd&lang=en'
		"""
		self.browser = webdriver.Chrome()

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

			username = (t.find('span', {'class':'username'}).get_text())
			link = ('https://twitter.com' + t.small.a['href'] if t.small is not None else '')
			date = (t.small.a['title'] if t.small is not None else '')
			stats = (t.find('div', {'class': 'ProfileTweet-actionList js-actions'}).get_text().replace('\n',''
				) if t.find('div', {'class': 'ProfileTweet-actionList js-actions'}) is not None else '')
			text = (t.p.get_text())
	            
			tweet = {
			'url': link,
			'user': username,
			'date': date,
			'stats': stats,
			'content': text,
			}
			tweets.append(tweet)

		return tweets