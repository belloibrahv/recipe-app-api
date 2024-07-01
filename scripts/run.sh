#!/bin/sh

set -e

# Wait for the database to be ready
echo "Waiting for database..."
python manage.py wait_for_db

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the uwsgi server
echo "Starting uwsgi server..."
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
