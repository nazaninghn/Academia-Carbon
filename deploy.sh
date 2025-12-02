#!/bin/bash

# Deployment Script for Academia Carbon v2.1.0
# Run this script to deploy to production

echo "========================================="
echo "Academia Carbon Deployment Script v2.1.0"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Step 2: Install/Update dependencies
echo ""
echo "Step 2: Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Step 3: Run tests
echo ""
echo "Step 3: Running deployment tests..."
python test_deployment.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests failed - Aborting deployment${NC}"
    exit 1
fi

# Step 4: Collect static files
echo ""
echo "Step 4: Collecting static files..."
python manage.py collectstatic --noinput --clear
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Static files collected${NC}"
else
    echo -e "${RED}✗ Failed to collect static files${NC}"
    exit 1
fi

# Step 5: Check deployment settings
echo ""
echo "Step 5: Checking deployment configuration..."
python manage.py check --deploy
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment check passed${NC}"
else
    echo -e "${YELLOW}⚠ Deployment check has warnings${NC}"
fi

# Step 6: Summary
echo ""
echo "========================================="
echo "Deployment Preparation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Deploy v2.1.0'"
echo "2. Push to repository: git push origin main"
echo "3. Deploy on your platform (Render/Heroku/VPS)"
echo "4. Run: python test_deployment.py on server"
echo ""
echo "For troubleshooting, see: SERVER_TROUBLESHOOTING.md"
echo ""
