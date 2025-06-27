#!/usr/bin/env bash

# One-time database setup script for interview-q
# Run this script only when you need to initialize the database

set -e  # Exit on any error

echo "🔧 Starting one-time database setup for interview-q..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    print_error "EB CLI is not installed. Please install it first:"
    echo "pip install awsebcli"
    exit 1
fi

# Ensure postgresql17 is installed (needed for psql command)
print_status "Ensuring postgresql17 is installed..."
eb ssh --command "sudo dnf install -y postgresql17 || echo 'postgresql17 may already be installed'"

# Create database if it doesn't exist
print_status "Creating database (if it doesn't exist)..."
eb ssh --command "set -a && source /opt/elasticbeanstalk/deployment/env && set +a && PGPASSWORD=\$RDS_PASSWORD psql -h \$RDS_HOSTNAME -U \$RDS_USERNAME -c \"CREATE DATABASE \$RDS_DB_NAME;\" || echo 'Database may already exist'"

# Run database migrations
print_status "Running database migrations..."
eb ssh --command "set -a && source /opt/elasticbeanstalk/deployment/env && set +a && source \$PYTHONPATH/activate && cd /var/app/current && python manage.py migrate"

# Collect static files
print_status "Collecting static files..."
eb ssh --command "set -a && source /opt/elasticbeanstalk/deployment/env && set +a && source \$PYTHONPATH/activate && cd /var/app/current && python manage.py collectstatic --noinput"

# Optional: Create superuser
read -p "Do you want to create a superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating superuser..."
    print_warning "You'll need to provide username, email, and password when prompted"
    eb ssh --command "source /var/app/venv/*/bin/activate && cd /var/app/current && python manage.py createsuperuser"
fi

print_status "✅ Database setup completed successfully!"
print_status "Your application should be available at:"
eb status | grep "CNAME" | awk '{print $2}'

echo ""
print_warning "This was a one-time setup. For future deployments, use the regular deploy script."
