# -*- coding: utf-8 -*-
"""
oauthlib.common
~~~~~~~~~~~~~~
This module provides data structures and utilities common
to all implementations of OAuth.
very important utility
"""

import collections
import datetime
import logging
import re
import time
import urllib.parse as urlparse

from urllib.parse import quote as _quote
from urllib.parse import unquote as _unquote
from urllib.parse import urlencode as _urlencode

try:
    from secrets import randbits
    from secrets import SystemRandom
except ImportError:
    from random import getrandbits as randbits
    from random import SystemRandom

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')

CLIENT_ID_CHARACTER_SET = (r' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN'
                           'OPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}')

SANITIZE_PATTERN = re.compile(r'([^&;]*(?:password|token)[^=]*=)[^&;]+', re.IGNORECASE)
INVALID_HEX_PATTERN = re.compile(r'%[^0-9A-Fa-f]|%[0-9A-Fa-f][^0-9A-Fa-f]')

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')






def urlencode(params):
    utf8_params = encode_params_utf8(params)
    urlencoded = _urlencode(utf8_params)
    if isinstance(urlencoded, str):
        return urlencoded
    else:
        return urlencoded.decode("utf-8")








def urldecode(query):
    """Decode a query string in x-www-form-urlencoded format into a sequence
    of two-element tuples.
    Unlike urlparse.parse_qsl(..., strict_parsing=True) urldecode will enforce
    correct formatting of the query string by validation. If validation fails
    a ValueError will be raised. urllib.parse_qsl will only raise errors if
    any of name-value pairs omits the equals sign.
    """
    # Check if query contains invalid characters
    if query and not set(query) <= urlencoded:
        error = ("Error trying to decode a non urlencoded string. "
                 "Found invalid characters: %s "
                 "in the string: '%s'. "
                 "Please ensure the request/response body is "
                 "x-www-form-urlencoded.")
        raise ValueError(error % (set(query) - urlencoded, query))

    # Check for correctly hex encoded values using a regular expression
    # All encoded values begin with % followed by two hex characters
    # correct = %00, %A0, %0A, %FF
    # invalid = %G0, %5H, %PO
    if INVALID_HEX_PATTERN.search(query):
        raise ValueError('Invalid hex encoding in query string.')

    # We want to allow queries such as "c2" whereas urlparse.parse_qsl
    # with the strict_parsing flag will not.
    params = urlparse.parse_qsl(query, keep_blank_values=True)

    # unicode all the things
    return decode_params_utf8(params)







def generate_timestamp():
    """Get seconds since epoch (UTC).
    Per `section 3.3`_ of the OAuth 1 RFC 5849 spec.
    Per `section 3.2.1`_ of the MAC Access Authentication spec.
    .. _`section 3.2.1`: https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01#section-3.2.1
    .. _`section 3.3`: https://tools.ietf.org/html/rfc5849#section-3.3
    """
    return str(int(time.time()))


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates a non-guessable OAuth token
    OAuth (1 and 2) does not specify the format of tokens except that they
    should be strings of random characters. Tokens should not be guessable
    and entropy when generating the random characters is important. Which is
    why SystemRandom is used instead of the default random.choice method.
    """
    rand = SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))





def generate_client_id(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates an OAuth client_id
    OAuth 2 specify the format of client_id in
    https://tools.ietf.org/html/rfc6749#appendix-A.
    """
    return generate_token(length, chars)

def generate_client_secret(length=20, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates an OAuth client_id
    OAuth 2 specify the format of client_id in
    https://tools.ietf.org/html/rfc6749#appendix-A.
    """
    return generate_token(length, chars)



def to_unicode(data, encoding='UTF-8'):
    """Convert a number of different types of objects to unicode."""
    if isinstance(data, str):
        return data

    if isinstance(data, bytes):
        return str(data, encoding=encoding)

    if hasattr(data, '__iter__'):
        try:
            dict(data)
        except TypeError:
            pass
        except ValueError:
            # Assume it's a one dimensional data structure
            return (to_unicode(i, encoding) for i in data)
        else:
            # We support 2.6 which lacks dict comprehensions
            if hasattr(data, 'items'):
                data = data.items()
            return {to_unicode(k, encoding): to_unicode(v, encoding) for k, v in data}

    return data



