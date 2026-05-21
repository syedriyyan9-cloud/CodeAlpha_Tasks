#!/bin/bash

echo "🔨 Building Django project for Vercel..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Verify staticfiles was created
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles directory created successfully"
else
    echo "❌ staticfiles directory missing! Creating it now..."
    mkdir -p staticfiles
fi

echo "✅ Build completed successfully!"