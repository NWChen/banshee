from banshee.scrapers.twitter_requests import Scrape

def test_get_by_username():
    """
    prints out the returned information
    """
    scrape = Scrape()
    statuses = scrape.get_by_username('realDonaldTrump')
    print(statuses)

def test_get_by_keywords():
    scrape = Scrape()
    statuses = scrape.get_by_keywords(['donald', 'trump'])
    print(statuses)

def test_retweets():
    scrape = Scrape()
    statuses = scrape.get_retweets(929717762422988801)
    print(statuses)

test_get_by_username()
print('done')
test_get_by_keywords()
print('done')
test_retweets()
print('done')
