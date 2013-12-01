#-*- coding:utf-8 -*-

import os
import sys

path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/urlhandler'
if path not in sys.path:
    sys.path.insert(1, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urlhandler.settings")

from django.core.handlers.wsgi import WSGIHandler
django_WSGI = WSGIHandler()

from queryhandler import handle_weixin_request
from settings import LUCKY_URL
from django.core import signals
from django.db import close_connection
signals.request_finished.connect(close_connection)

def app(environ, start_response):
    if environ['PATH_INFO'] == LUCKY_URL:
        result = handle_weixin_request(environ)
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return [result.encode('utf8')]
    else:
        #status = '200 OK'
        #headers = [('Content-type', 'text/html')]
        #start_response(status, headers)
        #return [environ['PATH_INFO']]
        return django_WSGI.__call__(environ, start_response)

