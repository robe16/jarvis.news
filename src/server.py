from bottle import request, run, route, get, post
from datetime import datetime

import cache
from config.config import get_cfg_port
from common_functions.request_enable_cors import enable_cors, response_options
from resources.global_resources.log_vars import logPass
from resources.lang.enGB.logs import *
from apis.get_config import get_config
from apis.get_headlines import get_headlines
from apis.get_sources import get_sources
from apis.get_news_config_html import get_news_config_html
from apis.get_news_config_js import get_news_config_js
from apis.post_news_config_update import post_news_config_update


def start_server():

    ################################################################################################
    # APIs
    ################################################################################################

    @route('/config', method=['OPTIONS'])
    @route('/news/headlines/<option>', method=['OPTIONS'])
    @route('/news/sources/<option>', method=['OPTIONS'])
    def api_cors_options(**kwargs):
        return response_options()

    @get('/config')
    def api_get_config():
        response = get_config(request)
        return enable_cors(response)

    @get('/news/headlines/<option>')
    def api_get_headlines(option):
        response = get_headlines(request, option)
        return enable_cors(response)

    @get('/news/sources/<option>')
    def api_get_sources(option):
        response = get_sources(request, option)
        return enable_cors(response)

    @get('/news/config.html')
    def api_get_news_config_html():
        response = get_news_config_html(request)
        return enable_cors(response)

    @get('/news/config.js')
    def api_get_news_config_js():
        response = get_news_config_js(request)
        return enable_cors(response)

    @post('/news/config/update')
    def api_post_news_config_update():
        response = post_news_config_update(request)
        return enable_cors(response)

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logPass,
                    'operation': logDescPortListener.format(port=port), 'description': 'started'})

    ################################################################################################
