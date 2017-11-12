from banshee.scrapers.api_setup import get_api
	
class Scrape(object):
	
	def __init__(self):
		self.api = get_api()

	def format_tweets(self, tweets):
		"""
		converts a list of tweet objects to a dict of only relevant data
		"""
		formatted_tweets = []

		for tweet in tweets:

			new_tweet = {}
			# new_tweet['location'] = tweet.place
			new_tweet['coordinates'] = tweet.coordinates
			new_tweet['content'] = tweet.text
			user = tweet.user
			new_tweet['name'] = user.name if user else None
			new_tweet['entities'] = tweet.entities
			new_tweet['language'] = tweet.lang
			new_tweet['retweet_count'] = tweet.retweet_count
			new_tweet['date'] = tweet.created_at

			formatted_tweets.append(new_tweet)

		return formatted_tweets

	def get_by_username(self, user_name:str, count=1):
		"""
		returns the most recent status of a username
		can return multiple statuses using count
		"""
		tweets = self.api.user_timeline(screen_name=user_name, count=count)

		return self.format_tweets(tweets)

	def get_by_keywords(self, keywords:list):
		"""
		uses a list of keywords to get related tweets
		"""
		keywords = ' OR '.join(keywords)
		tweets = self.api.search(q=keywords)
		return self.format_tweets(tweets)

	def get_retweets(self, tweet_id, count=1):
		"""
		returns up to the first 100 tweets of the given tweet
		"""
		tweets = self.api.retweets(id=tweet_id, count=count)
		return self.format_tweets(tweets)

	def get_by_location(self, geocode, language=None, since_id=None):
		"""
		geocode is latitude, longitude, radius
		language of tweets being retreived
		since_id tweet ids more recent than the param
		"""
		#self.api.search()
		pass