from banshee.scrapers.api_setup import get_api
	
class Scrape(object):
	
	def __init__(self):
		self.api = get_api()

	def get_by_username(self, user_name, count=1):
		"""
		returns the most recent status of a username
		can return multiple statuses using count
		returned tweet is formatted into a dict with only chosen values
		"""
		tweets = self.api.user_timeline(screen_name=user_name, count=count)

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