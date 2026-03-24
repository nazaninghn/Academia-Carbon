#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Collect static files
python manage.py collectstatic --noinput

# Compile translation messages (ignore errors if gettext not installed)
python manage.py compilemessages || echo "compilemessages skipped (gettext not installed)"

# Run migrations
python manage.py migrate

echo "Build completed successfully"