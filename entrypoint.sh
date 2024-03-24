#!/bin/sh
# exit on error
set -x
set -o errexit
echo "Install the dependencies"
pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#echo "Running Database Migrations"
#python manage.py createcachetable
#python manage.py migrate
echo "Running collectstatic commands"
python manage.py collectstatic --noinput

echo "Running app commands"
python manage.py runserver &
exec "$@"