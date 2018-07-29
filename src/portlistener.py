from bottle import get
from bottle import request, run

from config.config import get_cfg_port_listener
from log.log import log_internal
from resources.global_resources.log_vars import logPass
from resources.lang.enGB.logs import *
from service.news import News

from apis.get_config import get_config
from apis.get_headlines import get_headlines
from apis.get_sources import get_sources


def start_bottle():

    ################################################################################################
    # Create device
    ################################################################################################

    _newsapi = News()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

    @get('/config')
    def api_get_config():
        return get_config(request)

    @get('/news/headlines/<option>')
    def api_get_headlines(option):
        return get_headlines(request, _newsapi, option)

    @get('/news/sources/<option>')
    def api_get_sources(option):
        return get_sources(request, _newsapi, option)

    ################################################################################################

    host = 'localhost'
    port = get_cfg_port_listener()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
