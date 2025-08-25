#!/bin/bash

# MongoDB Restore Script
# This script restores a MongoDB database from backup

set -e

# Configuration
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

# Function to show usage
show_usage() {
    echo "Usage: $0 <backup_path> [options]"
    echo ""
    echo "Arguments:"
    echo "  backup_path    Path to the backup file or directory"
    echo ""
    echo "Options:"
    echo "  --drop         Drop existing collections before restore"
    echo "  --dry-run      Show what would be restored without actually doing it"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 ./backups/backup_userdb_20241201_143022"
    echo "  $0 ./backups/backup_userdb_20241201_143022.tar.gz"
    echo "  $0 ./backups/backup_userdb_20241201_143022 --drop"
}

# Parse command line arguments
BACKUP_PATH=""
DROP_COLLECTIONS=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --drop)
            DROP_COLLECTIONS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        -*)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            if [ -z "$BACKUP_PATH" ]; then
                BACKUP_PATH="$1"
            else
                print_error "Multiple backup paths specified"
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if backup path is provided
if [ -z "$BACKUP_PATH" ]; then
    print_error "Backup path is required"
    show_usage
    exit 1
fi

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

# Check if backup path exists
if [ ! -e "$BACKUP_PATH" ]; then
    print_error "Backup path does not exist: $BACKUP_PATH"
    exit 1
fi

print_status "Starting restore process..."
print_status "Database: $DB_NAME"
print_status "Backup path: $BACKUP_PATH"
print_status "Drop collections: $DROP_COLLECTIONS"
print_status "Dry run: $DRY_RUN"

# Handle compressed backups
if [[ "$BACKUP_PATH" == *.tar.gz ]]; then
    print_status "Detected compressed backup, extracting..."
    EXTRACT_DIR=$(mktemp -d)
    tar -xzf "$BACKUP_PATH" -C "$EXTRACT_DIR"
    BACKUP_PATH="$EXTRACT_DIR"
    print_status "Extracted to: $BACKUP_PATH"
fi

# Validate backup structure
if [ ! -d "$BACKUP_PATH/$DB_NAME" ]; then
    print_error "Invalid backup structure. Expected directory: $BACKUP_PATH/$DB_NAME"
    exit 1
fi

# List collections in backup
print_status "Collections found in backup:"
ls -la "$BACKUP_PATH/$DB_NAME/"

# Confirm restore (unless dry run)
if [ "$DRY_RUN" = false ]; then
    print_warning "This will overwrite existing data in the database!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Restore cancelled"
        exit 0
    fi
fi

# Copy backup to container
print_status "Copying backup to container..."
docker cp "$BACKUP_PATH" "$CONTAINER_NAME:/restore/"

# Perform restore
if [ "$DRY_RUN" = true ]; then
    print_status "DRY RUN: Would restore from: /restore/$(basename "$BACKUP_PATH")"
    print_status "DRY RUN: Would use database: $DB_NAME"
    if [ "$DROP_COLLECTIONS" = true ]; then
        print_status "DRY RUN: Would drop existing collections"
    fi
else
    print_status "Running mongorestore..."
    
    # Build restore command
    RESTORE_CMD="mongorestore --username $MONGO_ROOT_USERNAME --password $MONGO_ROOT_PASSWORD --authenticationDatabase admin --db $DB_NAME /restore/$(basename "$BACKUP_PATH")/$DB_NAME"
    
    if [ "$DROP_COLLECTIONS" = true ]; then
        RESTORE_CMD="$RESTORE_CMD --drop"
    fi
    
    # Execute restore
    docker exec "$CONTAINER_NAME" $RESTORE_CMD
    
    # Check if restore was successful
    if [ $? -eq 0 ]; then
        print_status "Restore completed successfully"
    else
        print_error "Restore failed"
        exit 1
    fi
fi

# Clean up
print_status "Cleaning up..."
docker exec "$CONTAINER_NAME" rm -rf "/restore/$(basename "$BACKUP_PATH")"

if [ -n "$EXTRACT_DIR" ] && [ -d "$EXTRACT_DIR" ]; then
    rm -rf "$EXTRACT_DIR"
fi

print_status "Restore process completed!"

# Show restore summary
if [ "$DRY_RUN" = false ]; then
    print_status "Restore summary:"
    print_status "  Database: $DB_NAME"
    print_status "  Collections restored: $(ls -1 "$BACKUP_PATH/$DB_NAME/" | wc -l)"
    print_status "  Drop mode: $DROP_COLLECTIONS"
fi
