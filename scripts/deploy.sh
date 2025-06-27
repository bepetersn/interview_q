#!/usr/bin/env bash

# Automated deployment script for interview-q
# This script deploys code and optionally runs setup tasks

set -e  # Exit on any error

echo "🚀 Starting deployment for interview-q..."

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

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    print_error "EB CLI is not installed. Please install it first:"
    echo "pip install awsebcli"
    exit 1
fi

# Check environment state before deploying
print_status "Checking environment state..."
ENV_STATUS=$(eb status | grep "Status:" | awk '{print $2}')
print_status "Current environment status: $ENV_STATUS"

if [ "$ENV_STATUS" != "Ready" ]; then
    print_error "Environment is not in Ready state (current: $ENV_STATUS)"
    print_error "Please wait for the environment to be Ready before deploying"
    print_warning "You can check status with: eb status"
    print_warning "Or monitor with: eb events --follow"
    exit 1
fi

# Deploy the application
print_status "Deploying application to Elastic Beanstalk..."
eb deploy

# Wait a moment for deployment to stabilize
print_status "Waiting for deployment to stabilize..."
sleep 10

# Setup SSH (required for new instances)
print_status "Setting up SSH access..."
./scripts/setup-ssh.sh

# Ask what setup tasks are needed
echo ""
echo "What setup tasks do you need to run?"
echo "1) Full database setup (create DB, migrate, collect static, create superuser)"
echo "2) Just run migrations"
echo "3) Just collect static files"
echo "4) Nothing (deployment only)"
echo ""
read -p "Choose an option (1-4): " -n 1 -r
echo

case $REPLY in
    1)
        print_status "Running full database setup..."
        ./scripts/setup-database.sh
        ;;
    2)
        print_status "Running database migrations..."
        eb ssh --command "set -a && source /opt/elasticbeanstalk/deployment/env && set +a && source \$PYTHONPATH/activate && cd /var/app/current && python manage.py migrate"
        ;;
    3)
        print_status "Collecting static files..."
        eb ssh --command "set -a && source /opt/elasticbeanstalk/deployment/env && set +a && source \$PYTHONPATH/activate && cd /var/app/current && python manage.py collectstatic --noinput"
        ;;
    4)
        print_status "Skipping setup tasks..."
        ;;
    *)
        print_warning "Invalid option. Skipping setup tasks..."
        ;;
esac

print_status "✅ Deployment completed successfully!"
print_status "Your application should be available at:"
eb status | grep "CNAME" | awk '{print $2}'
