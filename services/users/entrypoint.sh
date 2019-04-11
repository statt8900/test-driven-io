#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z users-db 5432; do
  sleep 0.1
done
sleep 4
echo "PostgresSQL started"

python manage.py run -h 0.0.0.0
