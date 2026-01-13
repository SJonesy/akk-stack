FROM nginx:alpine

# for htpasswd command
RUN apk add --no-cache apache2-utils || apk add --no-cache --update --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main apache2-utils

RUN rm -f /etc/nginx/conf.d/*

ENV SERVER_NAME=example.com
ENV PORT=80
ENV CLIENT_MAX_BODY_SIZE=1m
ENV PROXY_READ_TIMEOUT=60s
ENV WORKER_PROCESSES=1

COPY files/run.sh /
COPY files/nginx.conf.tmpl /
RUN chmod +x /run.sh

# use SIGQUIT for graceful shutdown
# c.f. http://nginx.org/en/docs/control.html
STOPSIGNAL SIGQUIT
ENTRYPOINT ["/run.sh"]

