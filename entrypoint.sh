#!/bin/sh

# Fix permissions on mounted volume (only if needed)
chown -R django_user:django_group /app

# Optionnel : run migrations automatically (décommente si tu veux)
# python manage.py migrate

# Démarre le service
exec "$@"
