from bottle import request, run, route

from config.config import get_cfg_port
from common_functions.request_enable_cors import enable_cors, response_options
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

    @route('/config', method=['OPTIONS', 'GET'])
    def api_get_config():
        if request.method == 'OPTIONS':
            response = response_options()
        else:
            response = get_config(request)
        return enable_cors(response)

    @route('/news/headlines/<option>', method=['OPTIONS', 'GET'])
    def api_get_headlines(option):
        response = get_headlines(request, _newsapi, option)
        return enable_cors(response)

    @route('/news/sources/<option>', method=['OPTIONS', 'GET'])
    def api_get_sources(option):
        response = get_sources(request, _newsapi, option)
        return enable_cors(response)

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
