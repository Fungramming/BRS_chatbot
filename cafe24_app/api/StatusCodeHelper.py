from flask_api import status

def statushelper(code):
    if code == 100:
        return status.HTTP_100_CONTINUE
    elif code == 101:
        return status.HTTP_101_SWITCHING_PROTOCOLS
    elif code == 200:
        return status.HTTP_200_OK
    elif code == 201:
        return status.HTTP_201_CREATED
    elif code == 202:
        return status.HTTP_202_ACCEPTED
    elif code == 203:
        return status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
    elif code == 204:
        return status.HTTP_204_NO_CONTENT
    elif code == 205:
        return status.HTTP_205_RESET_CONTENT
    elif code == 206:
        return status.HTTP_206_PARTIAL_CONTENT
    elif code == 207:
        return status.HTTP_207_MULTI_STATUS
    elif code == 300:
        return status.HTTP_300_MULTIPLE_CHOICES
    elif code == 301:
        return status.HTTP_301_MOVED_PERMANENTLY
    elif code == 302:
        return status.HTTP_302_FOUND
    elif code == 303:
        return status.HTTP_303_SEE_OTHER
    elif code == 304:
        return status.HTTP_304_NOT_MODIFIED
    elif code == 305:
        return status.HTTP_305_USE_PROXY
    elif code == 306:
        return status.HTTP_306_RESERVED
    elif code == 307:
        return status.HTTP_307_TEMPORARY_REDIRECT
    elif code == 308:
        return status.HTTP_308_PERMANENT_REDIRECT
    elif code == 400:
        return status.HTTP_400_BAD_REQUEST
    elif code == 401:
        return status.HTTP_401_UNAUTHORIZED
    elif code == 402:
        return status.HTTP_402_PAYMENT_REQUIRED
    elif code == 403:
        return status.HTTP_403_FORBIDDEN
    elif code == 404:
        return status.HTTP_404_NOT_FOUND
    elif code == 405:
        return status.HTTP_405_METHOD_NOT_ALLOWED
    elif code == 406:
        return status.HTTP_406_NOT_ACCEPTABLE
    elif code == 407:
        return status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED
    elif code == 408:
        return status.HTTP_408_REQUEST_TIMEOUT
    elif code == 409:
        return status.HTTP_409_CONFLICT
    elif code == 410:
        return status.HTTP_410_GONE
    elif code == 411:
        return status.HTTP_411_LENGTH_REQUIRED
    elif code == 412:
        return status.HTTP_412_PRECONDITION_FAILED
    elif code == 413:
        return status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    elif code == 414:
        return status.HTTP_414_REQUEST_URI_TOO_LONG
    elif code == 415:
        return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    elif code == 416:
        return status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
    elif code == 428:
        return status.HTTP_428_PRECONDITION_REQUIRED
    elif code == 429:
        return status.HTTP_429_TOO_MANY_REQUESTS
    elif code == 431:
        return status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
    elif code == 444:
        return status.HTTP_444_CONNECTION_CLOSED_WITHOUT_RESPONSE
    elif code == 500:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    elif code == 501:
        return status.HTTP_501_NOT_IMPLEMENTED
    elif code == 502:
        return status.HTTP_502_BAD_GATEWAY
    elif code == 503:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    elif code == 504:
        return status.HTTP_504_GATEWAY_TIMEOUT
    elif code == 505:
        return status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
    elif code == 508:
        return status.HTTP_508_LOOP_DETECTED
    elif code == 510:
        return status.HTTP_510_NOT_EXTENDED
    elif code == 511:
        return status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED