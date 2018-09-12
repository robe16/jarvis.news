import cache
from newsapi import NewsApiClient
from config.config import get_cfg_details_newsapiKey
from config.config import get_cfg_details_sources, get_cfg_details_categories, get_cfg_details_language, get_cfg_details_country


_newsapi = NewsApiClient(api_key=get_cfg_details_newsapiKey())


def cache_sources():
    cache.cache['sources'] = {}
    get_sources_for_sources()
    get_sources_for_categories()
    get_sources_for_language()
    get_sources_for_country()


def get_sources_for_sources():
    #
    sources = {}
    all_sources = get_sources_all()
    #
    for src in all_sources:
        if src in get_cfg_details_sources():
            sources[src] = src
    #
    cache.cache['sources']['sources'] = sources


def get_sources_all():
    #
    sources = _newsapi.get_sources()
    #
    return create_source_json(sources)


def get_sources_for_categories():
    #
    sources = {}
    #
    for cat in get_cfg_details_categories():
        sources[cat] = _get_sources_for_category(cat)
    #
    cache.cache['sources']['categories'] = sources


def _get_sources_for_category(category):
    #
    sources = _newsapi.get_sources(category=category)
    #
    return create_source_json(sources)


def get_sources_for_language():
    #
    sources = _newsapi.get_sources(language=get_cfg_details_language())
    #
    cache.cache['sources']['language'] = create_source_json(sources)


def get_sources_for_country():
    #
    sources = _newsapi.get_sources(country=get_cfg_details_country())
    #
    cache.cache['sources']['country'] = create_source_json(sources)


def create_source_json(sources):
    #
    _sources = {}
    #
    for source in sources['sources']:
        _sources[source['id']] = source
    #
    return _sources

