from banshee.scrapers.twitter_requests import Scrape

def test_get_by_username():
	"""
	prints out the returned information
	"""
	scrape = Scrape()
	statuses = scrape.get_by_username('realDonaldTrump')
	print(statuses)

test_get_by_username()