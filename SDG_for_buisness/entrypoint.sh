#!/bin/sh
set -e

echo "📦 Применяем миграции..."
ENV=docker python manage.py makemigrations --noinput
ENV=docker python manage.py migrate --noinput

ENV=docker python manage.py seed_relevance

echo "🚀 Запускаем сервер..."
exec "$@"
