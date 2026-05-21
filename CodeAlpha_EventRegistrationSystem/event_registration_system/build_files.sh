#!/bin/bash

echo "🔨 Building Django project for Vercel..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations (important for Supabase)
echo "💾 Running database migrations..."
python manage.py migrate --noinput

echo "✅ Build completed successfully!"