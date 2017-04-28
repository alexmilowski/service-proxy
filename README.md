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

There is a docker file for building an image for running the service.  Just create your configuration file (e.g., "myservice.conf") and then build the image:

```
docker build -t myservice --build-arg conf=myservice.conf .
```

The image uses a '/logs' directory for the service access and error logs. You'll want to map that to local filesystem.  Otherwise, the image is easy to run:

```
docker run -v `pwd`/logs:/logs -p :5000:5000 myservice
```

## Notes

Keep in mind that the service will respond to the host name you put into your configuration. If
you specify "`localhost`", it will only respond properly locally.  The service is based on Flask and you can read more about the configuration there as well.

Similarly, `gunicorn` has many configuration properties.  Any environment variable prefixed with `GUNICORN_` will be mapped in the `gunicorn.conf`.  Specifically, you can control the
number of workers with `GUNICORN_WORKERS`.
