#!/bin/bash
# Update script for ulga Django application

set -e  # Exit on error

echo "Starting deployment update..."

# Change to project directory
cd /home/ubuntu/ulga

# Pull latest changes
echo "Pulling latest changes from git..."
git pull origin main

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set production settings
export DJANGO_SETTINGS_MODULE=psi.settings_prod

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Restart gunicorn service
echo "Restarting gunicorn service..."
sudo systemctl restart ulga

# Check status
sleep 2
if sudo systemctl is-active --quiet ulga; then
    echo "✓ Deployment completed successfully!"
    echo "✓ Service is running"
else
    echo "✗ Warning: Service might not be running properly"
    echo "Check logs with: sudo journalctl -u ulga -n 50"
    exit 1
fi
