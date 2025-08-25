#!/bin/sh
set -e

echo "Starting FastAPI MongoDB application..."

# Wait for MongoDB to be ready
until python -c "
import asyncio
import motor.motor_asyncio
import os

async def check_mongo():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
        await client.admin.command('ping')
        print('MongoDB is ready!')
        return True
    except Exception as e:
        print(f'MongoDB not ready: {e}')
        return False

asyncio.run(check_mongo())
"
do
    echo "Waiting for MongoDB to be ready..."
    sleep 2
done

echo "All services are ready! Starting FastAPI application..."

# Start the FastAPI application with uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
