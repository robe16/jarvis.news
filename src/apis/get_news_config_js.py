from bottle import HTTPError, static_file
from datetime import datetime
import os

import cache
from common_functions.request_log_args import get_request_log_args
from resources.global_resources.log_vars import logPass, logException
from resources.global_resources.variables import *


def get_news_config_js(request):
    #
    args = get_request_log_args(request)
    args['timestamp'] = datetime.now()
    args['process'] = 'inbound'
    #
    try:
        #
        status = httpStatusSuccess
        args['result'] = logPass
        args['http_response_code'] = status
        args['description'] = '-'
        cache.logQ.put(args)
        #
        root = os.path.join(os.path.dirname(__file__), '..', 'service/config')
        response = static_file('config.js', root=root)
        response.status = status
        #
        return response
        #
    except Exception as e:
        #
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        cache.logQ.put(args)
        #
        raise HTTPError(status)
