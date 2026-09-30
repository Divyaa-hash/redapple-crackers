#!/bin/bash

# GoDaddy SSH Deployment Script
# This script deploys the crackers website to GoDaddy via SSH

# Configuration
SSH_HOST="redapplecrackers.com"
SSH_USER="gs26214tgb0g"
REMOTE_PATH="/home/gs26214tgb0g/redapple-crackers"
LOCAL_PATH="C:/Users/Divya/OneDrive/Desktop/crackers"

# Files to upload
FILES_TO_UPLOAD=(
    "db.sqlite3"
    "logo.jpg"
    "static/images/crackers/logo.jpg"
    "staticfiles/images/crackers/logo.jpg"
)

# Directories to sync (excluding certain files)
SYNC_EXCLUDES=(
    "--exclude=venv"
    "--exclude=__pycache__"
    "--exclude=.git"
    "--exclude=node_modules"
    "--exclude=*.pyc"
    "--exclude=.DS_Store"
    "--exclude=*.log"
)

echo "=========================================="
echo "GoDaddy SSH Deployment Script"
echo "=========================================="
echo "Host: $SSH_HOST"
echo "User: $SSH_USER"
echo "Remote Path: $REMOTE_PATH"
echo "=========================================="
echo ""

# Step 1: Backup existing database on remote server
echo "Step 1: Backing up existing database on GoDaddy..."
ssh $SSH_USER@$SSH_HOST "cd $REMOTE_PATH && cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
if [ $? -eq 0 ]; then
    echo "✓ Database backup completed"
else
    echo "✗ Database backup failed"
    exit 1
fi
echo ""

# Step 2: Upload database
echo "Step 2: Uploading database file..."
scp "$LOCAL_PATH/db.sqlite3" $SSH_USER@$SSH_HOST:$REMOTE_PATH/
if [ $? -eq 0 ]; then
    echo "✓ Database uploaded successfully"
else
    echo "✗ Database upload failed"
    exit 1
fi
echo ""

# Step 3: Upload logo files
echo "Step 3: Uploading logo files..."
scp "$LOCAL_PATH/logo.jpg" $SSH_USER@$SSH_HOST:$REMOTE_PATH/
scp "$LOCAL_PATH/static/images/crackers/logo.jpg" $SSH_USER@$SSH_HOST:$REMOTE_PATH/static/images/crackers/
scp "$LOCAL_PATH/staticfiles/images/crackers/logo.jpg" $SSH_USER@$SSH_HOST:$REMOTE_PATH/staticfiles/images/crackers/
if [ $? -eq 0 ]; then
    echo "✓ Logo files uploaded successfully"
else
    echo "✗ Logo files upload failed"
    exit 1
fi
echo ""

# Step 4: Sync static files
echo "Step 4: Syncing static files..."
rsync -avz "${SYNC_EXCLUDES[@]}" "$LOCAL_PATH/static/" $SSH_USER@$SSH_HOST:$REMOTE_PATH/static/
if [ $? -eq 0 ]; then
    echo "✓ Static files synced successfully"
else
    echo "✗ Static files sync failed"
    exit 1
fi
echo ""

# Step 5: Sync staticfiles (collected static)
echo "Step 5: Syncing collected static files..."
rsync -avz "${SYNC_EXCLUDES[@]}" "$LOCAL_PATH/staticfiles/" $SSH_USER@$SSH_HOST:$REMOTE_PATH/staticfiles/
if [ $? -eq 0 ]; then
    echo "✓ Collected static files synced successfully"
else
    echo "✗ Collected static files sync failed"
    exit 1
fi
echo ""

# Step 6: Restart Passenger application
echo "Step 6: Restarting Passenger application..."
ssh $SSH_USER@$SSH_HOST "cd $REMOTE_PATH && touch passenger_wsgi.py"
if [ $? -eq 0 ]; then
    echo "✓ Passenger restart triggered"
else
    echo "✗ Passenger restart failed"
    exit 1
fi
echo ""

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Visit http://redapplecrackers.com/ to verify"
echo "2. Check that the logo is updated"
echo "3. Check that product images are displaying correctly"
echo ""
