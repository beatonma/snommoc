ARG PYTHON_VERSION=3.13
ARG NODE_VERSION=24
ARG NGINX_VERSION=latest

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

ENTRYPOINT ["/entrypoint.sh"]

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
FROM nginx:${NGINX_VERSION} AS core_nginx
EXPOSE 80
EXPOSE 443

##################
#                #
#   Production   #
#                #
##################

# TODO

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
COPY tools/docker/django/django-entrypoint.dev.sh /
ENTRYPOINT ["/django-entrypoint.dev.sh"]

###
FROM core_celery AS dev_celery

###
FROM core_nginx AS dev_nginx

COPY ./tools/docker/nginx/templates/ /etc/nginx/templates/
COPY ./tools/docker/nginx/nginx.dev.conf /etc/nginx/nginx.conf
