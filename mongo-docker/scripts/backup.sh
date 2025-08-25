#!/bin/bash

# MongoDB Backup Script
# This script creates a backup of the MongoDB database

set -e

# Configuration
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
DB_NAME="${MONGO_DATABASE:-userdb}"
CONTAINER_NAME="mongo-docker-mongodb-1"

# MongoDB credentials from environment or defaults
MONGO_ROOT_USERNAME="${MONGO_ROOT_USERNAME:-admin}"
MONGO_ROOT_PASSWORD="${MONGO_ROOT_PASSWORD:-secure_password_123}"

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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if MongoDB container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    print_error "MongoDB container is not running. Please start the application first."
    exit 1
fi

# Create backup directory
print_status "Creating backup directory..."
mkdir -p "$BACKUP_DIR"

# Create backup filename
BACKUP_FILE="backup_${DB_NAME}_${DATE}"

print_status "Starting backup of database: $DB_NAME"
print_status "Backup file: $BACKUP_FILE"

# Perform backup using mongodump
print_status "Running mongodump..."
docker exec "$CONTAINER_NAME" mongodump \
    --username "$MONGO_ROOT_USERNAME" \
    --password "$MONGO_ROOT_PASSWORD" \
    --authenticationDatabase admin \
    --db "$DB_NAME" \
    --out "/dump/$BACKUP_FILE" \
    --gzip

# Check if backup was successful
if [ $? -eq 0 ]; then
    print_status "Backup completed successfully"
else
    print_error "Backup failed"
    exit 1
fi

# Copy backup from container to host
print_status "Copying backup from container to host..."
docker cp "$CONTAINER_NAME:/dump/$BACKUP_FILE" "$BACKUP_DIR/"

# Check if copy was successful
if [ $? -eq 0 ]; then
    print_status "Backup copied to host successfully"
else
    print_error "Failed to copy backup from container"
    exit 1
fi

# Clean up backup from container
print_status "Cleaning up container backup..."
docker exec "$CONTAINER_NAME" rm -rf "/dump/$BACKUP_FILE"

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)

print_status "Backup completed successfully!"
print_status "Location: $BACKUP_DIR/$BACKUP_FILE"
print_status "Size: $BACKUP_SIZE"

# Optional: Keep only last 10 backups
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR" | wc -l)
if [ "$BACKUP_COUNT" -gt 10 ]; then
    print_warning "More than 10 backups found. Removing oldest backups..."
    ls -t "$BACKUP_DIR" | tail -n +11 | xargs -I {} rm -rf "$BACKUP_DIR/{}"
    print_status "Old backups cleaned up"
fi

# Optional: Compress backup
if command -v tar > /dev/null 2>&1; then
    print_status "Compressing backup..."
    cd "$BACKUP_DIR"
    tar -czf "${BACKUP_FILE}.tar.gz" "$BACKUP_FILE"
    rm -rf "$BACKUP_FILE"
    print_status "Backup compressed: ${BACKUP_FILE}.tar.gz"
fi

print_status "Backup process completed!"
