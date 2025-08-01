#!/usr/bin/env ash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
python -m pytest -p no:cacheprovider || exit $?


python -m gunicorn snommoc.wsgi:application --bind 0.0.0.0:8000
