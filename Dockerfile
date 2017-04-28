FROM python:3.5
ARG conf

MAINTAINER Alex Miłowski <alex@milowski.com>

RUN pip install gunicorn Flask requests
COPY logging.conf /logging.conf
COPY gunicorn.conf /gunicorn.conf
COPY main.py /main.py
COPY proxy.py /proxy.py
COPY $conf /proxy.conf

ENV WEB_CONF "/proxy.conf"
ENV GUNICORN_WORKERS "4"

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":5000", "--log-file", "/logs/gunicorn.log", "--access-logfile", "/logs/access.log", "--error-logfile", "/logs/error.log","main:app"]
