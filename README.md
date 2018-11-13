# Web Service proxy

A simple "proxy aware" proxy for a web service.

## Overview

The service will forward HTTP requests to a web service allowing you to expose a remote service
via a local service.  In particular, you can configure the use of proxies for the
requests.  This allows you to navigate various "infrastructure" when access a web
service whilst developing an application.

## Usage

The configuration of the service is in the `proxy.conf` file:

 * `PROXIES`:  If you have proxies in play, just uncomment the `PROXIES` dictionary and add your proxy URLs.
 * `SERVER_NAME`: The host and port on which the service will respond.
 * `SERVICE`: The base URI of the service that is being proxied.
 * `VERIFY`: Just in case you have self-signed certificates in play ... change this to False.  Or get real certificates... please!

You can run the service via python directly:

```
export WEB_CONF=proxy.conf
python main.py
```

You can run the service via gunicorn:

```
export WEB_CONF=proxy.conf
export GUNICORN_WORKERS=4
gunicorn --config gunicorn.conf --log-config logging.conf -b ":5000" main:app
```

## Running in a Docker Container

There is a docker file for building an image for running the service.  The
configuration is expected to be in the /conf directory and logs are recorded
in the /logs directory.

You can use the public image alexmilowski/service-proxy:2018-11-13 or build
one yourself:

```
docker build -t service-proxy .
```

Adjust the configuration parameters in `conf/proxy.conf` and then run the
container of choice:


```
mkdir logs
docker run -v `pwd`/logs:/logs -v `pwd`/conf:/conf -p :5000:5000 service-proxy
```

## Notes

Keep in mind that the service will respond to the host name you put into your configuration. If
you specify "`localhost`", it will only respond properly locally.  The service
is based on Flask and you can read more about the configuration there as well.

Similarly, `gunicorn` has many configuration properties.  Any environment
variable prefixed with `GUNICORN_` will be mapped in the `gunicorn.conf`.  
Specifically, you can control the number of workers with `GUNICORN_WORKERS`.
