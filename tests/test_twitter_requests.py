import sys
import os
sys.path.append(os.getcwd() + '/../')
from scrapers.twitter_requests import TwitterRequests
from scrapers.twitter_searcher import TweetSearcher

def test_api_get_by_username():
    """
    prints out the returned information
    """
    scrape = TwitterRequests()
    statuses = scrape.get_by_username('realDonaldTrump')
    print(statuses)

def test_get_by_keywords():
    scrape = TwitterRequests()
    statuses = scrape.get_by_keywords(['donald', 'trump'])
    print(statuses)

def test_api_retweets():
    scrape = TwitterRequests()
    statuses = scrape.get_retweets(929717762422988801)
    print(statuses)

def test_tweet_searcher():
    search = TweetrSearcher('?q=donald%20trump&src=typd&lang=en')
    print(search.get_tweets(3))

test_tweet_searcher()
