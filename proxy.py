from flask import Flask, Response, stream_with_context,request
import requests
from requests.auth import HTTPBasicAuth
import sys

import io

from fixhtml import replaceuri
from codecs import iterdecode
from urllib.parse import unquote_plus


app = Flask(__name__)
app.config.from_envvar('WEB_CONF')
verify = app.config['VERIFY'] if 'VERIFY' in app.config else True
service = app.config['SERVICE']

if app.config.get('DEBUG_HTTP'):
   import logging

   # These two lines enable debugging at httplib level (requests->urllib3->http.client)
   # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
   # The only thing missing will be the response.body which is not logged.
   try:
       import http.client as http_client
   except ImportError:
       # Python 2
       import httplib as http_client
   http_client.HTTPConnection.debuglevel = 1

   # You must initialize logging, otherwise you'll not see debug output.
   logging.basicConfig()
   logging.getLogger().setLevel(logging.DEBUG)
   requests_log = logging.getLogger("requests.packages.urllib3")
   requests_log.setLevel(logging.DEBUG)
   requests_log.propagate = True

@app.route('/',methods=['GET','POST','PUT','DELETE'])
def index():
   return proxy('')

@app.route('/<path:path>',methods=['GET','POST','PUT','DELETE'])
def proxy(path):
   auth = None
   proxy_headers = {}
   for entry in request.headers:
      if entry[0] != 'Host' and \
         entry[0] != 'Authorization':
         proxy_headers[entry[0]] = entry[1]

   if request.authorization is not None:
      auth = HTTPBasicAuth(request.authorization.username,request.authorization.password)
   req = requests.request(
      request.method,service+path,
      data=request.data if request.method in ['POST','PUT'] else None,
      stream=True,
      params=request.args,
      cookies=request.cookies,
      proxies=app.config['PROXIES'] if 'PROXIES' in app.config else None,
      auth=auth,
      headers=proxy_headers,
      allow_redirects=False,
      verify=verify)
   response_headers = dict(req.headers)
   location = response_headers.get('Location')
   if location is not None and location[0:len(service)]==service:
      response_headers['Location'] = location[len(service):]
   response_headers.pop('Server',None)
   response_headers.pop('Date',None)
   response_headers.pop('Transfer-Encoding',None)
   response_headers.pop('Content-Length',None)
   lastModified = response_headers.get('Last-Modified')
   # Because some KNOX / Hadoop things are really broken
   if lastModified is not None:
      response_headers.pop('Last-Modified',None)
      response_headers['Last-Modified'] = unquote_plus(lastModified)
   contentType = response_headers.get('Content-Type')
   if contentType is not None and contentType[0:9]=='text/html':

      semicolon = contentType.find(';')
      encoding = 'UTF-8'
      if semicolon>0:
         params = contentType[semicolon+1:]
         pos = params.find('charset=')
         value = params[pos+8:]
         semicolon = value.find(';')
         encoding = value[0:semicolon] if semicolon>0 else value

      def textchunks():
         for chunk in iterdecode(req.iter_content(chunk_size=1024*32),encoding):
            yield chunk
      data = replaceuri(textchunks(),service,'/')
   else:
      data = req.iter_content(chunk_size=1024*32)

   #response = Response(stream_with_context(req.iter_content(chunk_size=1024*32)), headers=response_headers)
   response = Response(stream_with_context(data), headers=response_headers)
   response.status_code = req.status_code;
   return response

#if __name__ == '__main__':
#    app.run()
