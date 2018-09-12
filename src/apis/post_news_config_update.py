from bottle import HTTPError, HTTPResponse
from datetime import datetime

import cache
from config.config import set_cfg_details_updates
from common_functions.request_log_args import get_request_log_args
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from validation.validation import validate_config_update


def post_news_config_update(request):
    #
    args = get_request_log_args(request)
    args['timestamp'] = datetime.now()
    args['process'] = 'inbound'
    #
    try:
        #
        data = request.json
        #
        if validate_config_update(data):
            #
            r = set_cfg_details_updates(data['language'], data['country'], data['sources'], data['categories'])
            #
            if r:
                status = httpStatusSuccess
                logresult = logPass
            else:
                status = httpStatusFailure
                logresult = logFail
            #
        else:
            status = httpStatusBadrequest
            logresult = logPass
        #
        args['result'] = logresult
        args['http_response_code'] = status
        args['description'] = '-'
        cache.logQ.put(args)
        #
        response = HTTPResponse()
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
