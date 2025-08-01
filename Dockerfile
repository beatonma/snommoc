ARG PYTHON_VERSION=3.13
ARG NODE_VERSION=24
ARG NGINX_VERSION=1.29

##########################
#                        #
#   Common base stages   #
#                        #
##########################

###
FROM python:${PYTHON_VERSION}-alpine AS python
ENV PYTHONBUFFERED 1

###
FROM node:${NODE_VERSION}-alpine AS core_nextjs

RUN apk add --no-cache curl
WORKDIR /app
COPY ./frontend/package.json ./frontend/package-lock.json /app/
RUN npm ci && npm cache clean --force

COPY ./frontend /app

###
FROM python AS builder_django
WORKDIR /django/
COPY ./backend/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip,id=pipcache pip install -r ./requirements.txt
EXPOSE 8000

###
FROM python AS core_base_django
RUN \
    apk add --no-cache \
        binutils \
        curl \
        gcc \
        gdal \
        geos \
        geos-dev \
        libc-dev \
        proj \
    && if [ ! -e /usr/lib/libproj.so ]; then ln -s /usr/lib/libproj.so.* /usr/lib/libproj.so; fi \
    || if [ ! -e /usr/lib/libgdal.so ]; then ln -s /usr/lib/libgdal.so.* /usr/lib/libgdal.so; fi \
    || if [ ! -e /usr/lib/libgeos_c.so ]; then ln -s /usr/lib/libgeos_c.so.* /usr/lib/libgeos_c.so; fi

ARG PYTHON_VERSION
COPY --from=builder_django /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=builder_django /usr/local/bin/pytest /usr/local/bin/pytest

RUN addgroup -g 19283 docker_snommoc \
    && mkdir -p /var/log/snommoc/ \
    && chown :docker_snommoc /var/log/snommoc/ \
    && chmod 2775 /var/log/snommoc/

WORKDIR /django/
COPY ./backend /django

###
FROM core_base_django AS core_django

###
FROM core_base_django AS core_celery
ENTRYPOINT ["python", "-m", "celery", "-A", "snommoc", "worker", "-l", "info"]

###
FROM nginx:${NGINX_VERSION}-alpine AS core_nginx


###############################################################################
#                                                                             #
# Production DEMO                                                             #
# snommoc is currently deployed in 'demo' mode: publicly accessible but       #
# without scheduled data update tasks, user acccounts, or a dedicated         #
# server. Build requirements may change if true production status is reached. #
#                                                                             #
###############################################################################

FROM core_nextjs AS builder_productiondemo_nextjs
RUN npm run build

FROM node:${NODE_VERSION}-alpine AS productiondemo_nextjs

RUN apk add curl --no-cache
RUN addgroup -S app && adduser -S app -G app

USER app
WORKDIR /app

COPY --from=builder_productiondemo_nextjs --chown=app:app /app/.next/standalone ./
COPY --from=builder_productiondemo_nextjs --chown=app:app /app/package.json ./

ENV HOSTNAME="0.0.0.0"
ENV PORT="3000"
EXPOSE 3000
ENTRYPOINT ["node", "server.js"]

###
FROM core_django AS productiondemo_core_django
COPY ./backend /django

FROM productiondemo_core_django AS productiondemo_django

COPY tools/docker/django/entrypoint.prod.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && adduser -S django -G docker_snommoc \
    && mkdir -p /var/www/media \
    && mkdir -p /var/www/static \
    && chown -R :docker_snommoc /var/www/media /var/www/static \
    && chmod 2775 -R /var/www/
USER django
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

FROM productiondemo_core_django AS productiondemo_celery

RUN adduser -S celery -G docker_snommoc
USER celery

ENTRYPOINT ["python", "-m", "celery", "-A", "snommoc", "worker", "-l", "info"]

###
FROM core_nginx AS productiondemo_nginx

COPY tools/docker/nginx/nginx.prod-demo.conf /etc/nginx/nginx.conf
COPY ./tools/docker/nginx/templates /etc/nginx/templates

COPY --from=builder_productiondemo_nextjs --chown=nginx:nginx /app/.next/static /var/www/static-nextjs
COPY --from=builder_productiondemo_nextjs --chown=nginx:nginx /app/public /var/www/public-nextjs

EXPOSE 80

###################
#                 #
#   Development   #
#                 #
###################

###
FROM core_nextjs AS dev_nextjs
ENTRYPOINT ["npm", "run", "dev"]

###
FROM core_django AS dev_django
COPY tools/docker/django/entrypoint.dev.sh /
ENTRYPOINT ["/entrypoint.dev.sh"]

###
FROM core_celery AS dev_celery

###
FROM core_nginx AS dev_nginx

COPY ./tools/docker/nginx/templates/ /etc/nginx/templates/
COPY ./tools/docker/nginx/nginx.dev.conf /etc/nginx/nginx.conf


EXPOSE 80

###############
#             #
#   Testing   #
#             #
###############
###
FROM dev_django AS test_django

###
FROM productiondemo_nextjs AS test_nextjs

###
FROM productiondemo_nginx AS test_nginx
