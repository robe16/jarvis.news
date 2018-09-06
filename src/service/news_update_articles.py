from time import sleep
from datetime import datetime

import cache
from newsapi import NewsApiClient
from service.news_getinfo import cache_sources
from config.config import get_cfg_details_newsapiKey, get_cfg_details_sources
# from config.config import get_cfg_details_categories, get_cfg_details_language, get_cfg_details_country
from resources.global_resources.log_vars import logPass, logFail
from resources.lang.enGB.logs import *

# newsapi.org request limit is "1,000 requests per day", which averages at 1 request every 86 seconds
retrieval_frequency = 600  # 10 minutes


def newsUpdater_service():
    #
    _newsapi = NewsApiClient(api_key=get_cfg_details_newsapiKey())
    #
    cache_sources()
    #
    while True:
        cache.cache['headlines'] = {}
        #
        ####
        # Sources
        sources = ','.join(get_cfg_details_sources())
        data = _newsapi.get_top_headlines(sources=sources)
        #
        cache.cache['headlines']['sources'] = data['articles']
        #
        # Logging
        result = logPass if data['status'] == 'ok' else logFail
        cache.logQ.put({'timestamp': datetime.now(),
                        'process': 'outbound', 'result': result,
                        'service_ip': logDesc_newsapi_url_base,
                        'service_port': '',
                        'service_method': 'GET',
                        'service_request_uri': logDesc_newsapi_uri_topheadlines,
                        'service_request_query': 'sources={sources}'.format(sources=sources),
                        'service_request_body': '-',
                        'http_response_code': 'unknown',
                        'description': '-'})
        #
        ####
        # Categories
        # data = {}
        # for category in get_cfg_details_categories():
        #     data[category] = _newsapi.get_top_headlines(category=category)
        #     #
        #     # Logging
        #     result = logPass if data['status'] == 'ok' else logFail
        #     cache.logQ.put({'timestamp': datetime.now(),
        #                     'process': 'outbound', 'result': result,
        #                     'service_ip': logDesc_newsapi_url_base,
        #                     'service_port': '',
        #                     'service_method': 'GET',
        #                     'service_request_uri': logDesc_newsapi_uri_topheadlines,
        #                     'service_request_query': 'category={category}'.format(category=category),
        #                     'service_request_body': '-',
        #                     'http_response_code': 'unknown',
        #                     'description': '-'})
        #
        # cache.cache['headlines']['categories'] = data['articles']
        #
        cache.cache['headlines']['categories'] = {}
        #
        ####
        # Language
        # language = get_cfg_details_language()
        # data = _newsapi.get_top_headlines(language=language)
        #
        # cache.cache['headlines']['language'] = data['articles']
        #
        # Logging
        # result = logPass if data['status'] == 'ok' else logFail
        # cache.logQ.put({'timestamp': datetime.now(),
        #                 'process': 'outbound', 'result': result,
        #                 'service_ip': logDesc_newsapi_url_base,
        #                 'service_port': '',
        #                 'service_method': 'GET',
        #                 'service_request_uri': logDesc_newsapi_uri_topheadlines,
        #                 'service_request_query': 'language={language}'.format(language=language),
        #                 'service_request_body': '-',
        #                 'http_response_code': 'unknown',
        #                 'description': '-'})
        #
        cache.cache['headlines']['language'] = {}
        #
        ####
        # Country
        # country = get_cfg_details_country()
        # data = _newsapi.get_top_headlines(country=country)
        #
        # cache.cache['headlines']['country'] = data['articles']
        #
        # Logging
        # result = logPass if data['status'] == 'ok' else logFail
        # cache.logQ.put({'timestamp': datetime.now(),
        #                 'process': 'outbound', 'result': result,
        #                 'service_ip': logDesc_newsapi_url_base,
        #                 'service_port': '',
        #                 'service_method': 'GET',
        #                 'service_request_uri': logDesc_newsapi_uri_topheadlines,
        #                 'service_request_query': 'articles={articles}'.format(articles=articles),
        #                 'service_request_body': '-',
        #                 'http_response_code': 'unknown',
        #                 'description': '-'})
        #
        cache.cache['headlines']['country'] = {}
        #
        sleep(retrieval_frequency)
