#!/usr/bin/env bash

# SSH setup script for interview-q Elastic Beanstalk environment
# Use this when you need to setup SSH access to your EB environment

set -e  # Exit on any error

echo "🔐 Setting up SSH access to interview-q environment..."

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "EB CLI is not installed. Please install it first:"
    echo "pip install awsebcli"
    exit 1
fi

# Setup SSH automatically (non-interactive)
print_status "Setting up SSH access..."
echo -e "interview-q-env\n1\n" | eb ssh --setup

print_status "✅ SSH setup completed successfully!"
print_status "You can now use 'eb ssh' to connect to your environment"
