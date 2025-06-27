#!/bin/bash

# Exit on error
set -e

# Navigate into the Django project
cd ai_hunt

# Install dependencies
pip install -r requirements.txt

# Collect static files into static_root
python manage.py collectstatic --noinput

# Prepare Vercel static build directory
mkdir -p staticfiles_build/static
cp -r static_root/* staticfiles_build/static/