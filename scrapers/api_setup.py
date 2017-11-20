import tweepy

consumer_key = 'GqrtpC3erxpZv7tdBBEus2MHk'
consumer_secret = 'Ir2bFz8D9dfCT1F1zZpAHCJPWBO5xYPIdWcsvXy2kFzElZbdJw'
access_token = '928826177736904705-sFin3mNUlpg16b5XZ99B6RlD5YAD1jx'
access_token_secret = 'oQ37sdti1WH6HrzPLi9CPscaogGjdffvrlSpIYSoDWJGb'


def get_api():
	"""
	sets up the tweepy and twitter api auth, returns the tweepy object
	"""
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	return api
