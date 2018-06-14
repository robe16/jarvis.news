import threading

from bottle import HTTPError
from bottle import get
from bottle import request, run, HTTPResponse

from config.config import get_cfg_port_listener
from log.log import log_inbound, log_internal
from resources.global_resources.exposed_apis import *
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from resources.lang.enGB.logs import *
from service.news import News

from apis.uri_config import get_config
from apis.uri_get_headlines import get_headlines
from apis.uri_get_sources import get_sources


def start_bottle(port_threads):

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

    def bottle_run(x_host, x_port):
        log_internal(logPass, logDescPortListener.format(port=x_port), description='started')
        run(host=x_host, port=x_port, debug=True)

    ################################################################################################

    host = 'localhost'
    ports = get_cfg_port_listener()
    for port in ports:
        t = threading.Thread(target=bottle_run, args=(host, port,))
        port_threads.append(t)

    # Start all threads
    for t in port_threads:
        t.start()
    # Use .join() for all threads to keep main process 'alive'
    for t in port_threads:
        t.join()
