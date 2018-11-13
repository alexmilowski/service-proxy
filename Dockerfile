FROM python:3.7
ARG conf

MAINTAINER Alex Miłowski <alex@milowski.com>

RUN pip install gunicorn Flask requests
COPY logging.conf /logging.conf
COPY gunicorn.conf /gunicorn.conf
COPY main.py /main.py
COPY proxy.py /proxy.py
COPY fixhtml.py /fixhtml.py
RUN mkdir /conf /logs; touch /conf/proxy.conf

ENV WEB_CONF "/conf/proxy.conf"
ENV GUNICORN_WORKERS "8"
ENV GUNICORN_TIMEOUT "180"

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":5000", "--log-file", "/logs/gunicorn.log", "--access-logfile", "/logs/access.log", "--error-logfile", "/logs/error.log","main:app"]
