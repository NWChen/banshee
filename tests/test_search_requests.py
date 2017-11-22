import sys
import os
import pprint
sys.path.append(os.getcwd() + '/../')

from scrapers.search_requests import Requests 

requests = Requests()
pprint.pprint(requests.search_user('realdonaldtrump'))
print('done')
pprint.pprint(requests.search_location('chicago', 10))
print('done')
pprint.pprint(requests.search_exact_keywords(['chipotle', 'subway']))
print('done')
pprint.pprint(requests.search_partial_keywords(['chipotle', 'racism']))
print('done')
pprint.pprint(requests.search_exact_phrase('i love fridays'))
print('done')
pprint.pprint(requests.search_exact_keywords_by_location(['chipotle', 'subway'], 'chicago'))
print('done')
