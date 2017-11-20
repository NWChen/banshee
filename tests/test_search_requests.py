import sys
import os
import pprint
sys.path.append(os.getcwd() + '/../')

from scrapers.search_requests import Requests 


pprint.pprint(Requests.search_user('realdonaldtrump'))
print('done')
pprint.pprint(Requests.search_location('chicago', 20))
print('done')
pprint.pprint(Requests.search_exact_keywords(['chipotle', 'subway']))
print('done')
pprint.pprint(Requests.search_partial_keywords(['chipotle', 'racism']))
print('done')
pprint.pprint(Requests.search_exact_phrase('i love fridays'))
print('done')
pprint.pprint(Requests.search_exact_keywords_by_location(['chipotle', 'subway'], 'chicago'))
print('done')
