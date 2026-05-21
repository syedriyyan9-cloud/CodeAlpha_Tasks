#!/bin/bash

echo "🔨 Building Django project for Vercel..."

# Install dependencies
pip install -r requirements.txt

# Run migrations (creates tables in Supabase)
echo "💾 Running database migrations..."
python manage.py migrate --noinput

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Build completed!"