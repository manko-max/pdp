// MongoDB initialization script
// This script runs when MongoDB container starts for the first time

// Switch to the application database
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE || 'userdb');

// Create application user with limited permissions
db.createUser({
    user: process.env.MONGO_APP_USERNAME || 'appuser',
    pwd: process.env.MONGO_APP_PASSWORD || 'app_password_123',
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_INITDB_DATABASE || 'userdb'
        }
    ]
});

// Switch back to admin database to create root user if not exists
db = db.getSiblingDB('admin');

// Create root user if not exists
try {
    db.createUser({
        user: process.env.MONGO_ROOT_USERNAME || 'admin',
        pwd: process.env.MONGO_ROOT_PASSWORD || 'secure_password_123',
        roles: [
            {
                role: 'userAdminAnyDatabase',
                db: 'admin'
            },
            {
                role: 'readWriteAnyDatabase',
                db: 'admin'
            },
            {
                role: 'dbAdminAnyDatabase',
                db: 'admin'
            }
        ]
    });
    print('Root user created successfully');
} catch (error) {
    if (error.code === 51003) {
        print('Root user already exists');
    } else {
        print('Error creating root user: ' + error.message);
    }
}

// Switch back to application database
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE || 'userdb');

// Create collections with validation
db.createCollection('users', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'email', 'status', 'created_at', 'updated_at'],
            properties: {
                name: {
                    bsonType: 'string',
                    description: 'User name - required'
                },
                email: {
                    bsonType: 'string',
                    pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
                    description: 'Valid email address - required'
                },
                age: {
                    bsonType: ['int', 'null'],
                    minimum: 0,
                    maximum: 150,
                    description: 'User age - optional, must be positive'
                },
                status: {
                    enum: ['active', 'inactive', 'suspended'],
                    description: 'User status - required'
                },
                created_at: {
                    bsonType: 'date',
                    description: 'Creation timestamp - required'
                },
                updated_at: {
                    bsonType: 'date',
                    description: 'Last update timestamp - required'
                }
            }
        }
    }
});

// Create indexes for better performance
db.users.createIndex({ 'email': 1 }, { unique: true });
db.users.createIndex({ 'created_at': -1 });
db.users.createIndex({ 'status': 1, 'created_at': -1 });
db.users.createIndex({ 'name': 'text', 'email': 'text' });

// Create sessions collection for session storage
db.createCollection('sessions', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['session_id', 'user_id', 'created_at', 'expires_at'],
            properties: {
                session_id: {
                    bsonType: 'string',
                    description: 'Session identifier - required'
                },
                user_id: {
                    bsonType: 'string',
                    description: 'User identifier - required'
                },
                data: {
                    bsonType: 'object',
                    description: 'Session data - optional'
                },
                created_at: {
                    bsonType: 'date',
                    description: 'Session creation time - required'
                },
                expires_at: {
                    bsonType: 'date',
                    description: 'Session expiration time - required'
                }
            }
        }
    }
});

// Create indexes for sessions
db.sessions.createIndex({ 'session_id': 1 }, { unique: true });
db.sessions.createIndex({ 'user_id': 1 });
db.sessions.createIndex({ 'expires_at': 1 }, { expireAfterSeconds: 0 });

// Create audit log collection
db.createCollection('audit_logs', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['action', 'user_id', 'timestamp', 'ip_address'],
            properties: {
                action: {
                    enum: ['create', 'read', 'update', 'delete', 'login', 'logout'],
                    description: 'Action performed - required'
                },
                user_id: {
                    bsonType: 'string',
                    description: 'User identifier - required'
                },
                resource_type: {
                    bsonType: 'string',
                    description: 'Type of resource affected - optional'
                },
                resource_id: {
                    bsonType: 'string',
                    description: 'Resource identifier - optional'
                },
                details: {
                    bsonType: 'object',
                    description: 'Additional details - optional'
                },
                ip_address: {
                    bsonType: 'string',
                    description: 'IP address - required'
                },
                user_agent: {
                    bsonType: 'string',
                    description: 'User agent string - optional'
                },
                timestamp: {
                    bsonType: 'date',
                    description: 'Action timestamp - required'
                }
            }
        }
    }
});

// Create indexes for audit logs
db.audit_logs.createIndex({ 'timestamp': -1 });
db.audit_logs.createIndex({ 'user_id': 1, 'timestamp': -1 });
db.audit_logs.createIndex({ 'action': 1, 'timestamp': -1 });

// Insert sample data for testing
db.users.insertMany([
    {
        name: 'John Doe',
        email: 'john.doe@example.com',
        age: 30,
        status: 'active',
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        name: 'Jane Smith',
        email: 'jane.smith@example.com',
        age: 25,
        status: 'active',
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        name: 'Bob Johnson',
        email: 'bob.johnson@example.com',
        age: 35,
        status: 'inactive',
        created_at: new Date(),
        updated_at: new Date()
    }
]);

print('MongoDB initialization completed successfully!');
print('Database: ' + process.env.MONGO_INITDB_DATABASE || 'userdb');
print('Collections created: users, sessions, audit_logs');
print('Sample users inserted: 3');
