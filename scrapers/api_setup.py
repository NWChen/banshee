import tweepy

consumer_key = '' # need to create one for use
consumer_secret = '' # need to create one for use
access_token = '' # need to create one for use
access_token_secret = '' # need to create one for use


def get_api():
	"""
	sets up the tweepy and twitter api auth, returns the tweepy object
	"""
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	return api
