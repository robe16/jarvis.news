from bottle import HTTPResponse, HTTPError
from datetime import datetime

import cache
from common_functions.request_log_args import get_request_log_args
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from service.config.config_page import build_page


def get_news_config_html(request):
    #
    args = get_request_log_args(request)
    args['timestamp'] = datetime.now()
    args['process'] = 'inbound'
    #
    try:
        #
        data = {}
        #
        body = build_page()
        #
        if not bool(body):
            status = httpStatusFailure
            args['result'] = logFail
        else:
            status = httpStatusSuccess
            args['result'] = logPass
        #
        args['http_response_code'] = status
        args['description'] = '-'
        cache.logQ.put(args)
        #
        response = HTTPResponse()
        response.status = status
        #
        if not isinstance(data, bool):
            response.body = body
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
