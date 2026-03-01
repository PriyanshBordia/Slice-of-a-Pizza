#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import socket, sys
try:
    s = socket.create_connection(('db', 5432), timeout=2)
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    echo "  PostgreSQL not ready, waiting..."
    sleep 2
done
echo "PostgreSQL is ready."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

exec "$@"
