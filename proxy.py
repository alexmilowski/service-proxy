from flask import Flask, Response, stream_with_context,request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_envvar('WEB_CONF')
verify = app.config['VERIFY'] if 'VERIFY' in app.config else True
service = app.config['SERVICE']

@app.route('/',methods=['GET','POST','PUT','DELETE'])
def index():
   return proxy('')

@app.route('/<path:path>',methods=['GET','POST','PUT','DELETE'])
def proxy(path):
   auth = None
   #print(request.data)
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
      verify=verify)
   #print(req.headers)
   response = Response(stream_with_context(req.iter_content(chunk_size=1024*32)), headers=dict(req.headers))
   response.status_code = req.status_code;
   return response

#if __name__ == '__main__':
#    app.run()
