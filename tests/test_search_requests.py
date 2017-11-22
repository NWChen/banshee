import sys
import os
import pprint
sys.path.append(os.getcwd() + '/../')

from scrapers.search_requests import Requests 

requests = Requests()
pprint.pprint(requests.search_user('realdonaldtrump')[0])
print('done')
pprint.pprint(requests.search_location('chicago', 10)[0])
print('done')
pprint.pprint(requests.search_exact_keywords(['chipotle', 'subway'])[0])
print('done')
pprint.pprint(requests.search_partial_keywords(['chipotle', 'racism'])[0])
print('done')
pprint.pprint(requests.search_exact_phrase('i love fridays')[0])
print('done')
pprint.pprint(requests.search_exact_keywords_by_location(['chipotle', 'subway'], 'chicago')[0])
print('done')
pprint.pprint(requests.search_partial_keywords_by_location(['chipotle', 'subway'], 'chicago')[0])
print('done')
pprint.pprint(requests.search_exact_phrase_by_location('its so cold', 'chicago', 2)[0])
print('done')
pprint.pprint(requests.search_exact_keywords_by_username(['hate'], '@realdonaldtrump')[0])
print('done')
pprint.pprint(requests.search_partial_keywords_by_username(['hate', 'heart'], 'realdonaldtrump')[0])
print('done')
pprint.pprint(requests.search_exact_phrase_by_username('I love', 'realdonaldtrump')[0])
print('done')
