from bottle import HTTPResponse, HTTPError
from datetime import datetime

import cache
from common_functions.request_log_args import get_request_log_args
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def get_headlines(request, option):
    #
    args = get_request_log_args(request)
    args['timestamp'] = datetime.now()
    args['process'] = 'inbound'
    #
    try:
        #
        data = {}
        #
        if option == 'sources':
            data['articles'] = cache.cache['headlines']['sources']
            data['sources'] = cache.cache['sources']['sources']
        elif option == 'categories':
            data['articles'] = cache.cache['headlines']['categories']
            data['sources'] = cache.cache['sources']['categories']
        elif option == 'country':
            data['articles'] = cache.cache['headlines']['country']
            data['sources'] = cache.cache['sources']['country']
        elif option == 'language':
            data['articles'] = cache.cache['headlines']['language']
            data['sources'] = cache.cache['sources']['language']
        else:
            data = False
        #
        if not bool(data):
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
            response.body = data
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
