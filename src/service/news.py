from newsapi import NewsApiClient

from config.config import get_cfg_details_newsapiKey
from config.config import get_cfg_details_language, get_cfg_details_country, get_cfg_details_sources, get_cfg_details_categories
from log.log import log_outbound, log_internal
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.lang.enGB.logs import *


class Nest():

    def __init__(self):
        #
        self._newsapi = NewsApiClient(api_key=get_cfg_details_newsapiKey())

    def get_news_headlines_sources(self):
        #
        _sources = ','.join(get_cfg_details_sources())
        _uri = '/{uri}?{query}'.format(uri=logDesc_newsapi_uri_topheadlines,
                                       query='sources={sources}'.format(sources=_sources))
        #
        data = self._newsapi.get_top_headlines(sources=_sources)
        #
        result = logPass if data['status'] == 'ok' else logFail
        #
        log_outbound(result,
                     logDesc_newsapi_url_base, '', 'GET', _uri, '-', '-',
                     'unknown')
        #
        if data['status'] == 'ok':
            return {'articles': data['articles']}
        else:
            return False

    def get_news_headlines_language(self):
        #
        _uri = '/{uri}?{query}'.format(uri=logDesc_newsapi_uri_topheadlines,
                                       query='language={language}'.format(language=get_cfg_details_language()))
        #
        data = self._newsapi.get_top_headlines(language=get_cfg_details_language())
        #
        result = logPass if data['status'] == 'ok' else logFail
        #
        log_outbound(result,
                     logDesc_newsapi_url_base, '', 'GET', _uri, '-', '-',
                     'unknown')
        #
        if data['status'] == 'ok':
            return {'articles': data['articles']}
        else:
            return False

    def get_news_headlines_country(self):
        #
        _uri = '/{uri}?{query}'.format(uri=logDesc_newsapi_uri_topheadlines,
                                       query='country={country}'.format(country=get_cfg_details_country()))
        #
        data = self._newsapi.get_top_headlines(country=get_cfg_details_country())
        #
        result = logPass if data['status'] == 'ok' else logFail
        #
        log_outbound(result,
                     logDesc_newsapi_url_base, '', 'GET', _uri, '-', '-',
                     'unknown')
        #
        if data['status'] == 'ok':
            return {'articles': data['articles']}
        else:
            return False

    def get_news_headlines_categories(self):
        #
        data = []
        #
        for category in get_cfg_details_categories():
            #
            _uri = '/{uri}?{query}'.format(uri=logDesc_newsapi_uri_topheadlines,
                                           query='category={category}'.format(category=category))
            #
            data_cat = self._newsapi.get_top_headlines(category=category,
                                                       country=get_cfg_details_country())
            #
            result = logPass if data_cat['status'] == 'ok' else logFail
            #
            log_outbound(result,
                         logDesc_newsapi_url_base, '', 'GET', _uri, '-', '-',
                         'unknown')
            #
            if data_cat['status'] == 'ok':
                data = data + data_cat['articles']
        #
        if len(data):
            return {'articles': data}
        else:
            return False
