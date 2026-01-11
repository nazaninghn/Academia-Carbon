#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️  Running migrations..."
python manage.py migrate

echo "🌐 Compiling translation messages..."
python manage.py compilemessages

echo "📊 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔍 Running Django checks..."
python manage.py check --deploy

echo "✅ Build completed successfully!"
