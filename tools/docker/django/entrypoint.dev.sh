#!/usr/bin/env ash

python manage.py migrate
python manage.py collectstatic --noinput
pytest -p no:cacheprovider

python manage.py runserver_plus 0.0.0.0:8000
