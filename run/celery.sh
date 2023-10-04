python manage.py migrate --no-input;
celery -A Blog worker -c 2 -l INFO