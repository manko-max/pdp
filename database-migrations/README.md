# Database Migrations

## What is a database migration?

A **database migration** is a script or set of instructions that defines changes to a database schema. It's a way to version control your database structure and apply incremental changes to keep your database schema in sync with your application code.

### Key Concepts:
- **Schema Evolution**: Gradual changes to database structure over time
- **Version Control**: Track database changes like code changes
- **Reproducibility**: Apply same changes across different environments
- **Rollback Capability**: Undo changes if needed

## Why are database migrations important in application development?

### 1. **Schema Version Control**
- Track all database changes over time
- Maintain consistency across environments
- Enable team collaboration on database changes

### 2. **Environment Synchronization**
- Keep development, staging, and production databases in sync
- Ensure all team members have the same database structure
- Prevent "works on my machine" issues

### 3. **Deployment Automation**
- Automate database updates during application deployment
- Reduce manual database management errors
- Ensure consistent deployment process

### 4. **Team Collaboration**
- Multiple developers can work on database changes
- Merge conflicts in database schema are handled properly
- Clear history of who made what changes

### 5. **Rollback Capability**
- Undo problematic changes quickly
- Maintain database integrity during rollbacks
- Reduce downtime during issues

## What might a typical database migration include?

### Common Migration Types:

#### 1. **Create Table**
```python
# Python with SQLAlchemy/Alembic
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    op.drop_table('users')
```

#### 2. **Add Column**
```python
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

#### 3. **Modify Column**
```python
def upgrade():
    op.alter_column('users', 'email',
        existing_type=sa.String(100),
        type_=sa.String(150),
        nullable=False
    )

def downgrade():
    op.alter_column('users', 'email',
        existing_type=sa.String(150),
        type_=sa.String(100),
        nullable=False
    )
```

#### 4. **Create Index**
```python
def upgrade():
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', 'users')
```

#### 5. **Add Foreign Key**
```python
def upgrade():
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
    op.drop_column('orders', 'user_id')
```

#### 6. **Data Migration**
```python
def upgrade():
    # Add new column
    op.add_column('users', sa.Column('full_name', sa.String(200), nullable=True))
    
    # Migrate existing data
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = CONCAT(first_name, ' ', last_name)"
    )
    
    # Make column not nullable
    op.alter_column('users', 'full_name', nullable=False)

def downgrade():
    op.drop_column('users', 'full_name')
```

## How do database migrations help with version control of a database's schema?

### 1. **Migration Files as Version Control**
```bash
# Migration file naming convention
migrations/
├── 001_create_users_table.py
├── 002_add_user_phone.py
├── 003_create_orders_table.py
├── 004_add_order_status.py
└── 005_create_indexes.py
```

### 2. **Migration Tracking Table**
```sql
-- Most migration tools create a tracking table
CREATE TABLE schema_migrations (
    version VARCHAR(255) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example entries
INSERT INTO schema_migrations VALUES 
('001_create_users_table', '2024-01-15 10:30:00'),
('002_add_user_phone', '2024-01-15 11:15:00'),
('003_create_orders_table', '2024-01-15 14:20:00');
```

### 3. **Version Control Integration**
```python
# Migration with version control metadata
"""
Revision ID: 001_create_users_table
Revises: 
Create Date: 2024-01-15 10:30:00.000000
Author: John Doe
Description: Create users table with basic fields
"""

def upgrade():
    # Migration code here
    pass

def downgrade():
    # Rollback code here
    pass
```

### 4. **Branch-based Migrations**
```bash
# Feature branch migrations
feature/user-authentication/
├── 006_add_user_roles.py
├── 007_create_permissions_table.py
└── 008_add_role_permissions.py

feature/order-management/
├── 009_create_order_items_table.py
├── 010_add_order_tracking.py
└── 011_create_payment_methods.py
```

## Can you explain the difference between an "up" migration and a "down" migration?

### **Up Migration (Upgrade)**
- **Purpose**: Apply changes to the database
- **Direction**: Forward in time
- **Usage**: Deploy new features, add tables, modify schema
- **Example**: Add a new column to existing table

```python
def upgrade():
    """Apply changes to database schema"""
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.create_index('idx_users_last_login', 'users', ['last_login'])
```

### **Down Migration (Downgrade)**
- **Purpose**: Undo changes from the database
- **Direction**: Backward in time
- **Usage**: Rollback problematic changes, revert to previous state
- **Example**: Remove a column that was added

```python
def downgrade():
    """Undo changes from database schema"""
    op.drop_index('idx_users_last_login', 'users')
    op.drop_column('users', 'last_login')
```

### **Migration Flow Example**
```python
# Migration: 002_add_user_phone.py
def upgrade():
    """Add phone column to users table"""
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.create_index('idx_users_phone', 'users', ['phone'])

def downgrade():
    """Remove phone column from users table"""
    op.drop_index('idx_users_phone', 'users')
    op.drop_column('users', 'phone')

# Migration: 003_make_phone_required.py
def upgrade():
    """Make phone column required"""
    # First, ensure all users have phone numbers
    connection = op.get_bind()
    connection.execute("UPDATE users SET phone = 'N/A' WHERE phone IS NULL")
    
    # Then make column not nullable
    op.alter_column('users', 'phone', nullable=False)

def downgrade():
    """Make phone column optional again"""
    op.alter_column('users', 'phone', nullable=True)
```

## What could potentially go wrong during a database migration? How might you mitigate these risks?

### **Common Migration Risks:**

#### 1. **Data Loss**
```python
# RISKY: Dropping column without backup
def upgrade():
    op.drop_column('users', 'old_field')  # Data lost forever!

# SAFER: Rename column instead
def upgrade():
    op.alter_column('users', 'old_field', new_column_name='old_field_backup')
    # Later migration can drop it after verification
```

#### 2. **Locking Issues**
```python
# RISKY: Adding NOT NULL column to large table
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50), nullable=False))
    # This locks the entire table during migration

# SAFER: Add nullable first, then populate, then make required
def upgrade():
    # Step 1: Add nullable column
    op.add_column('users', sa.Column('new_field', sa.String(50), nullable=True))
    
    # Step 2: Populate data in batches
    connection = op.get_bind()
    connection.execute("UPDATE users SET new_field = 'default_value' WHERE new_field IS NULL")
    
    # Step 3: Make required
    op.alter_column('users', 'new_field', nullable=False)
```

#### 3. **Foreign Key Violations**
```python
# RISKY: Adding foreign key without checking data
def upgrade():
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])
    # Fails if orders.user_id references non-existent users

# SAFER: Validate data first
def upgrade():
    connection = op.get_bind()
    
    # Check for orphaned records
    orphaned = connection.execute("""
        SELECT COUNT(*) FROM orders o 
        LEFT JOIN users u ON o.user_id = u.id 
        WHERE u.id IS NULL
    """).scalar()
    
    if orphaned > 0:
        raise Exception(f"Found {orphaned} orphaned orders. Clean up data first.")
    
    # Add foreign key
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])
```

#### 4. **Performance Issues**
```python
# RISKY: Creating index on large table during peak hours
def upgrade():
    op.create_index('idx_users_email', 'users', ['email'])
    # This can take hours on large tables

# SAFER: Create index concurrently
def upgrade():
    op.create_index('idx_users_email', 'users', ['email'], postgresql_concurrently=True)
    # Non-blocking index creation
```

### **Risk Mitigation Strategies:**

#### 1. **Backup Strategy**
```python
def upgrade():
    # Create backup before risky operations
    connection = op.get_bind()
    connection.execute("CREATE TABLE users_backup AS SELECT * FROM users")
    
    try:
        # Perform risky migration
        op.alter_column('users', 'email', type_=sa.String(200))
    except Exception as e:
        # Restore from backup
        connection.execute("DROP TABLE users")
        connection.execute("ALTER TABLE users_backup RENAME TO users")
        raise e
```

#### 2. **Staged Migrations**
```python
# Migration 1: Add column
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50), nullable=True))

# Migration 2: Populate data
def upgrade():
    connection = op.get_bind()
    connection.execute("UPDATE users SET new_field = 'default_value'")

# Migration 3: Make required
def upgrade():
    op.alter_column('users', 'new_field', nullable=False)
```

#### 3. **Validation Checks**
```python
def upgrade():
    connection = op.get_bind()
    
    # Pre-migration validation
    user_count = connection.execute("SELECT COUNT(*) FROM users").scalar()
    if user_count == 0:
        raise Exception("No users found. Migration may not be needed.")
    
    # Perform migration
    op.add_column('users', sa.Column('status', sa.String(20), nullable=False, server_default='active'))
    
    # Post-migration validation
    null_status = connection.execute("SELECT COUNT(*) FROM users WHERE status IS NULL").scalar()
    if null_status > 0:
        raise Exception("Migration failed: some users have null status")
```

#### 4. **Rollback Planning**
```python
def upgrade():
    # Always implement proper downgrade
    op.add_column('users', sa.Column('temporary_field', sa.String(50), nullable=True))

def downgrade():
    # Ensure rollback is safe
    connection = op.get_bind()
    
    # Check if column is still needed
    usage_count = connection.execute("SELECT COUNT(*) FROM users WHERE temporary_field IS NOT NULL").scalar()
    if usage_count > 0:
        raise Exception("Cannot rollback: temporary_field is still in use")
    
    op.drop_column('users', 'temporary_field')
```

## What are some tools or libraries commonly used for managing database migrations?

### **Python Tools:**

#### 1. **Alembic (SQLAlchemy)**
```python
# alembic.ini configuration
[alembic]
script_location = migrations
sqlalchemy.url = postgresql://user:pass@localhost/db

# Migration file
"""Add user phone number

Revision ID: 002_add_user_phone
Revises: 001_create_users
Create Date: 2024-01-15 10:30:00
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

#### 2. **Django Migrations**
```python
# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)

# Migration file: 0002_user_phone.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
```

#### 3. **Flask-Migrate**
```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Migration commands
# flask db init
# flask db migrate -m "Add user phone"
# flask db upgrade
```

### **Other Language Tools:**

#### 4. **Laravel Migrations (PHP)**
```php
<?php
// Migration file: 2024_01_15_103000_add_phone_to_users_table.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddPhoneToUsersTable extends Migration
{
    public function up()
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('phone', 20)->nullable();
        });
    }

    public function down()
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('phone');
        });
    }
}
```

#### 5. **ActiveRecord Migrations (Ruby)**
```ruby
# Migration file: 20240115103000_add_phone_to_users.rb
class AddPhoneToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :phone, :string, limit: 20
  end
end
```

#### 6. **Flyway (Java)**
```sql
-- Migration file: V002__Add_phone_to_users.sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Rollback file: U002__Remove_phone_from_users.sql
ALTER TABLE users DROP COLUMN phone;
```

#### 7. **Liquibase (Java)**
```xml
<!-- Migration file: 002-add-phone-to-users.xml -->
<changeSet id="002-add-phone-to-users" author="developer">
    <addColumn tableName="users">
        <column name="phone" type="varchar(20)"/>
    </addColumn>
</changeSet>
```

### **Database-Specific Tools:**

#### 8. **PostgreSQL**
```sql
-- Manual migration script
BEGIN;
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
CREATE INDEX idx_users_phone ON users(phone);
COMMIT;
```

#### 9. **MySQL**
```sql
-- Manual migration script
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
CREATE INDEX idx_users_phone ON users(phone);
```

## Can you describe a situation where you might need to perform a database migration?

### **Scenario 1: Adding New Feature**
```python
# Situation: Adding user profile pictures to existing user system
# Current schema: users table with basic fields
# New requirement: Store profile picture URLs

def upgrade():
    """Add profile picture support to users"""
    # Add new column
    op.add_column('users', sa.Column('profile_picture_url', sa.String(500), nullable=True))
    
    # Add index for performance
    op.create_index('idx_users_profile_picture', 'users', ['profile_picture_url'])
    
    # Create new table for picture metadata
    op.create_table('user_pictures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('picture_url', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    """Remove profile picture support"""
    op.drop_table('user_pictures')
    op.drop_index('idx_users_profile_picture', 'users')
    op.drop_column('users', 'profile_picture_url')
```

### **Scenario 2: Performance Optimization**
```python
# Situation: Slow queries on orders table
# Problem: No indexes on frequently queried columns
# Solution: Add strategic indexes

def upgrade():
    """Add performance indexes to orders table"""
    # Add index on user_id (foreign key)
    op.create_index('idx_orders_user_id', 'orders', ['user_id'])
    
    # Add index on status (frequently filtered)
    op.create_index('idx_orders_status', 'orders', ['status'])
    
    # Add composite index for common queries
    op.create_index('idx_orders_user_status', 'orders', ['user_id', 'status'])
    
    # Add index on created_at for date range queries
    op.create_index('idx_orders_created_at', 'orders', ['created_at'])

def downgrade():
    """Remove performance indexes"""
    op.drop_index('idx_orders_created_at', 'orders')
    op.drop_index('idx_orders_user_status', 'orders')
    op.drop_index('idx_orders_status', 'orders')
    op.drop_index('idx_orders_user_id', 'orders')
```

### **Scenario 3: Data Structure Refactoring**
```python
# Situation: Changing from single address field to structured address
# Current: users.address (TEXT)
# New: Separate fields for street, city, state, zip

def upgrade():
    """Refactor address structure"""
    # Add new address columns
    op.add_column('users', sa.Column('street_address', sa.String(200), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('state', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('zip_code', sa.String(20), nullable=True))
    
    # Migrate existing data
    connection = op.get_bind()
    connection.execute("""
        UPDATE users 
        SET street_address = SPLIT_PART(address, ',', 1),
            city = SPLIT_PART(address, ',', 2),
            state = SPLIT_PART(address, ',', 3),
            zip_code = SPLIT_PART(address, ',', 4)
        WHERE address IS NOT NULL
    """)
    
    # Drop old column
    op.drop_column('users', 'address')

def downgrade():
    """Revert address structure"""
    # Add back old column
    op.add_column('users', sa.Column('address', sa.Text(), nullable=True))
    
    # Migrate data back
    connection = op.get_bind()
    connection.execute("""
        UPDATE users 
        SET address = CONCAT_WS(', ', street_address, city, state, zip_code)
        WHERE street_address IS NOT NULL
    """)
    
    # Drop new columns
    op.drop_column('users', 'zip_code')
    op.drop_column('users', 'state')
    op.drop_column('users', 'city')
    op.drop_column('users', 'street_address')
```

### **Scenario 4: Security Enhancement**
```python
# Situation: Adding password security features
# Current: Simple password field
# New: Password hashing, salt, reset tokens

def upgrade():
    """Enhance password security"""
    # Add password hash field
    op.add_column('users', sa.Column('password_hash', sa.String(255), nullable=True))
    
    # Add salt field
    op.add_column('users', sa.Column('password_salt', sa.String(255), nullable=True))
    
    # Add password reset token
    op.add_column('users', sa.Column('reset_token', sa.String(255), nullable=True))
    
    # Add token expiration
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True))
    
    # Migrate existing passwords (hash them)
    connection = op.get_bind()
    users = connection.execute("SELECT id, password FROM users WHERE password IS NOT NULL")
    
    for user in users:
        # Hash existing password
        salt = generate_salt()
        password_hash = hash_password(user.password, salt)
        
        connection.execute("""
            UPDATE users 
            SET password_hash = %s, password_salt = %s
            WHERE id = %s
        """, (password_hash, salt, user.id))
    
    # Drop old password column
    op.drop_column('users', 'password')

def downgrade():
    """Revert password security"""
    # Add back old column
    op.add_column('users', sa.Column('password', sa.String(100), nullable=True))
    
    # Note: Cannot recover original passwords from hashes
    # This is a one-way migration for security reasons
    connection = op.get_bind()
    connection.execute("UPDATE users SET password = 'MIGRATED_PASSWORD'")
    
    # Drop new columns
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'password_salt')
    op.drop_column('users', 'password_hash')
```

## How can database migrations be used to maintain data integrity?

### **1. Constraint Enforcement**
```python
def upgrade():
    """Add data integrity constraints"""
    # Add check constraint for email format
    op.create_check_constraint(
        'ck_users_email_format',
        'users',
        "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
    )
    
    # Add check constraint for phone format
    op.create_check_constraint(
        'ck_users_phone_format',
        'users',
        "phone ~ '^\\+?[1-9]\\d{1,14}$'"
    )
    
    # Add check constraint for age
    op.create_check_constraint(
        'ck_users_age_positive',
        'users',
        'age > 0 AND age < 150'
    )

def downgrade():
    """Remove data integrity constraints"""
    op.drop_constraint('ck_users_age_positive', 'users', type_='check')
    op.drop_constraint('ck_users_phone_format', 'users', type_='check')
    op.drop_constraint('ck_users_email_format', 'users', type_='check')
```

### **2. Foreign Key Relationships**
```python
def upgrade():
    """Add foreign key constraints"""
    # Ensure all orders have valid users
    op.create_foreign_key(
        'fk_orders_user_id',
        'orders', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # Ensure all order items have valid orders
    op.create_foreign_key(
        'fk_order_items_order_id',
        'order_items', 'orders',
        ['order_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # Ensure all order items have valid products
    op.create_foreign_key(
        'fk_order_items_product_id',
        'order_items', 'products',
        ['product_id'], ['id'],
        ondelete='RESTRICT'
    )

def downgrade():
    """Remove foreign key constraints"""
    op.drop_constraint('fk_order_items_product_id', 'order_items', type_='foreignkey')
    op.drop_constraint('fk_order_items_order_id', 'order_items', type_='foreignkey')
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
```

### **3. Data Validation and Cleanup**
```python
def upgrade():
    """Clean up invalid data"""
    connection = op.get_bind()
    
    # Remove duplicate emails
    connection.execute("""
        DELETE FROM users 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM users 
            GROUP BY email
        )
    """)
    
    # Fix invalid phone numbers
    connection.execute("""
        UPDATE users 
        SET phone = NULL 
        WHERE phone !~ '^\\+?[1-9]\\d{1,14}$'
    """)
    
    # Fix invalid ages
    connection.execute("""
        UPDATE users 
        SET age = NULL 
        WHERE age <= 0 OR age >= 150
    """)
    
    # Add unique constraint after cleanup
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

def downgrade():
    """Remove unique constraint"""
    op.drop_constraint('uq_users_email', 'users', type_='unique')
```

### **4. Referential Integrity**
```python
def upgrade():
    """Ensure referential integrity"""
    connection = op.get_bind()
    
    # Remove orphaned order items
    connection.execute("""
        DELETE FROM order_items 
        WHERE order_id NOT IN (SELECT id FROM orders)
    """)
    
    # Remove orphaned orders
    connection.execute("""
        DELETE FROM orders 
        WHERE user_id NOT IN (SELECT id FROM users)
    """)
    
    # Add foreign key constraints
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_order_items_order_id', 'order_items', 'orders', ['order_id'], ['id'])

def downgrade():
    """Remove foreign key constraints"""
    op.drop_constraint('fk_order_items_order_id', 'order_items', type_='foreignkey')
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
```

### **5. Data Type Consistency**
```python
def upgrade():
    """Ensure data type consistency"""
    connection = op.get_bind()
    
    # Convert string prices to decimal
    connection.execute("""
        UPDATE products 
        SET price = CAST(price AS DECIMAL(10,2))
        WHERE price ~ '^[0-9]+\\.?[0-9]*$'
    """)
    
    # Remove invalid price entries
    connection.execute("""
        UPDATE products 
        SET price = 0.00 
        WHERE price IS NULL OR price !~ '^[0-9]+\\.?[0-9]*$'
    """)
    
    # Change column type
    op.alter_column('products', 'price',
        existing_type=sa.String(20),
        type_=sa.Decimal(10, 2),
        nullable=False
    )

def downgrade():
    """Revert data type changes"""
    op.alter_column('products', 'price',
        existing_type=sa.Decimal(10, 2),
        type_=sa.String(20),
        nullable=False
    )
```

## Why is it important to test database migrations before applying them to a production database?

### **1. Data Safety**
```python
# Test migration on copy of production data
def test_migration_safety():
    """Test migration on production data copy"""
    # Create test database with production data
    test_db = create_test_database()
    copy_production_data(test_db)
    
    try:
        # Run migration
        run_migration('002_add_user_phone', test_db)
        
        # Verify data integrity
        assert_no_data_loss(test_db)
        assert_constraints_valid(test_db)
        assert_performance_acceptable(test_db)
        
        print("Migration test passed!")
        
    except Exception as e:
        print(f"Migration test failed: {e}")
        raise
    finally:
        cleanup_test_database(test_db)
```

### **2. Performance Testing**
```python
def test_migration_performance():
    """Test migration performance on large dataset"""
    # Create test database with large dataset
    test_db = create_test_database()
    generate_large_dataset(test_db, 1000000)  # 1M records
    
    start_time = time.time()
    
    try:
        # Run migration
        run_migration('003_add_indexes', test_db)
        
        duration = time.time() - start_time
        
        # Check if migration completed within acceptable time
        assert duration < 300, f"Migration took {duration}s, expected < 300s"
        
        print(f"Migration completed in {duration}s")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        raise
    finally:
        cleanup_test_database(test_db)
```

### **3. Rollback Testing**
```python
def test_migration_rollback():
    """Test migration rollback functionality"""
    test_db = create_test_database()
    
    try:
        # Run migration
        run_migration('004_add_user_roles', test_db)
        
        # Verify migration worked
        assert_table_exists(test_db, 'user_roles')
        assert_column_exists(test_db, 'users', 'role_id')
        
        # Test rollback
        rollback_migration('004_add_user_roles', test_db)
        
        # Verify rollback worked
        assert_table_not_exists(test_db, 'user_roles')
        assert_column_not_exists(test_db, 'users', 'role_id')
        
        print("Migration rollback test passed!")
        
    except Exception as e:
        print(f"Migration rollback test failed: {e}")
        raise
    finally:
        cleanup_test_database(test_db)
```

### **4. Integration Testing**
```python
def test_migration_integration():
    """Test migration with application code"""
    test_db = create_test_database()
    
    try:
        # Run migration
        run_migration('005_add_user_preferences', test_db)
        
        # Test application code with new schema
        app = create_test_application(test_db)
        
        # Test user creation
        user = app.create_user('test@example.com', 'password')
        assert user.id is not None
        
        # Test user preferences
        user.set_preference('theme', 'dark')
        assert user.get_preference('theme') == 'dark'
        
        print("Migration integration test passed!")
        
    except Exception as e:
        print(f"Migration integration test failed: {e}")
        raise
    finally:
        cleanup_test_database(test_db)
```

### **5. Automated Testing Pipeline**
```python
# CI/CD pipeline for migration testing
def migration_test_pipeline():
    """Automated migration testing pipeline"""
    migrations = get_pending_migrations()
    
    for migration in migrations:
        print(f"Testing migration: {migration.name}")
        
        # Test on empty database
        test_empty_database(migration)
        
        # Test on sample data
        test_sample_data(migration)
        
        # Test on production data copy
        test_production_data_copy(migration)
        
        # Test rollback
        test_rollback(migration)
        
        # Test performance
        test_performance(migration)
        
        print(f"Migration {migration.name} passed all tests!")
    
    print("All migrations passed testing!")
```

## What are seeds?

**Seeds** are scripts that populate a database with initial or test data. They are used to set up a database with predefined data that is necessary for the application to function properly.

### **Purpose of Seeds:**
- **Initial Data**: Set up required data for application startup
- **Test Data**: Provide sample data for development and testing
- **Reference Data**: Insert lookup tables, categories, and configuration data
- **User Data**: Create default users, roles, and permissions

## What data could be placed in seeds?

### **1. Reference Data**
```python
# seeds/reference_data.py
def seed_reference_data():
    """Seed reference data"""
    # Countries
    countries = [
        {'code': 'US', 'name': 'United States'},
        {'code': 'CA', 'name': 'Canada'},
        {'code': 'GB', 'name': 'United Kingdom'},
        {'code': 'DE', 'name': 'Germany'},
        {'code': 'FR', 'name': 'France'},
    ]
    
    for country in countries:
        db.session.add(Country(**country))
    
    # Categories
    categories = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Clothing', 'description': 'Apparel and fashion items'},
        {'name': 'Books', 'description': 'Books and educational materials'},
        {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
    ]
    
    for category in categories:
        db.session.add(Category(**category))
    
    db.session.commit()
```

### **2. User Roles and Permissions**
```python
# seeds/user_roles.py
def seed_user_roles():
    """Seed user roles and permissions"""
    # Roles
    roles = [
        {'name': 'admin', 'description': 'System administrator'},
        {'name': 'user', 'description': 'Regular user'},
        {'name': 'moderator', 'description': 'Content moderator'},
        {'name': 'guest', 'description': 'Guest user'},
    ]
    
    for role_data in roles:
        role = Role(**role_data)
        db.session.add(role)
    
    db.session.commit()
    
    # Permissions
    permissions = [
        {'name': 'create_user', 'description': 'Create new users'},
        {'name': 'edit_user', 'description': 'Edit user information'},
        {'name': 'delete_user', 'description': 'Delete users'},
        {'name': 'view_users', 'description': 'View user list'},
        {'name': 'manage_products', 'description': 'Manage products'},
        {'name': 'view_orders', 'description': 'View orders'},
    ]
    
    for perm_data in permissions:
        permission = Permission(**perm_data)
        db.session.add(permission)
    
    db.session.commit()
    
    # Assign permissions to roles
    admin_role = Role.query.filter_by(name='admin').first()
    user_permissions = Permission.query.filter(Permission.name.like('user_%')).all()
    
    for permission in user_permissions:
        admin_role.permissions.append(permission)
    
    db.session.commit()
```

### **3. Default Users**
```python
# seeds/default_users.py
def seed_default_users():
    """Seed default users"""
    # Admin user
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password_hash=hash_password('admin123'),
        role_id=Role.query.filter_by(name='admin').first().id,
        is_active=True,
        email_verified=True
    )
    db.session.add(admin_user)
    
    # Test users
    test_users = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'user'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'role': 'user'
        },
        {
            'username': 'moderator',
            'email': 'mod@example.com',
            'password': 'password123',
            'role': 'moderator'
        }
    ]
    
    for user_data in test_users:
        role = Role.query.filter_by(name=user_data['role']).first()
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=hash_password(user_data['password']),
            role_id=role.id,
            is_active=True,
            email_verified=True
        )
        db.session.add(user)
    
    db.session.commit()
```

### **4. Product Data**
```python
# seeds/product_data.py
def seed_product_data():
    """Seed product data"""
    # Product categories
    electronics = Category.query.filter_by(name='Electronics').first()
    clothing = Category.query.filter_by(name='Clothing').first()
    
    # Sample products
    products = [
        {
            'name': 'iPhone 15',
            'description': 'Latest iPhone with advanced features',
            'price': 999.99,
            'category_id': electronics.id,
            'sku': 'IPHONE15-001',
            'stock_quantity': 50
        },
        {
            'name': 'Samsung Galaxy S24',
            'description': 'Premium Android smartphone',
            'price': 899.99,
            'category_id': electronics.id,
            'sku': 'SAMSUNG-S24-001',
            'stock_quantity': 30
        },
        {
            'name': 'Nike Air Max',
            'description': 'Comfortable running shoes',
            'price': 129.99,
            'category_id': clothing.id,
            'sku': 'NIKE-AM-001',
            'stock_quantity': 100
        },
        {
            'name': 'Adidas T-Shirt',
            'description': 'Comfortable cotton t-shirt',
            'price': 29.99,
            'category_id': clothing.id,
            'sku': 'ADIDAS-TS-001',
            'stock_quantity': 200
        }
    ]
    
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
```

### **5. Configuration Data**
```python
# seeds/configuration.py
def seed_configuration():
    """Seed configuration data"""
    configs = [
        {'key': 'site_name', 'value': 'My E-commerce Store', 'type': 'string'},
        {'key': 'site_description', 'value': 'The best online store', 'type': 'string'},
        {'key': 'max_upload_size', 'value': '10485760', 'type': 'integer'},  # 10MB
        {'key': 'allowed_file_types', 'value': 'jpg,jpeg,png,gif,pdf', 'type': 'string'},
        {'key': 'email_notifications', 'value': 'true', 'type': 'boolean'},
        {'key': 'maintenance_mode', 'value': 'false', 'type': 'boolean'},
        {'key': 'default_currency', 'value': 'USD', 'type': 'string'},
        {'key': 'tax_rate', 'value': '0.08', 'type': 'decimal'},
    ]
    
    for config_data in configs:
        config = Configuration(**config_data)
        db.session.add(config)
    
    db.session.commit()
```

### **6. Sample Orders**
```python
# seeds/sample_orders.py
def seed_sample_orders():
    """Seed sample orders"""
    # Get test users
    john = User.query.filter_by(username='john_doe').first()
    jane = User.query.filter_by(username='jane_smith').first()
    
    # Get products
    iphone = Product.query.filter_by(sku='IPHONE15-001').first()
    nike_shoes = Product.query.filter_by(sku='NIKE-AM-001').first()
    
    # Create sample orders
    orders = [
        {
            'user_id': john.id,
            'status': 'completed',
            'total_amount': 999.99,
            'items': [
                {'product_id': iphone.id, 'quantity': 1, 'price': 999.99}
            ]
        },
        {
            'user_id': jane.id,
            'status': 'pending',
            'total_amount': 129.99,
            'items': [
                {'product_id': nike_shoes.id, 'quantity': 1, 'price': 129.99}
            ]
        }
    ]
    
    for order_data in orders:
        order = Order(
            user_id=order_data['user_id'],
            status=order_data['status'],
            total_amount=order_data['total_amount']
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items
        for item_data in order_data['items']:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['price']
            )
            db.session.add(order_item)
    
    db.session.commit()
```

### **7. Complete Seed Function**
```python
# seeds/__init__.py
def run_all_seeds():
    """Run all seed functions"""
    print("Seeding database...")
    
    try:
        seed_reference_data()
        print("✓ Reference data seeded")
        
        seed_user_roles()
        print("✓ User roles seeded")
        
        seed_default_users()
        print("✓ Default users seeded")
        
        seed_product_data()
        print("✓ Product data seeded")
        
        seed_configuration()
        print("✓ Configuration seeded")
        
        seed_sample_orders()
        print("✓ Sample orders seeded")
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Database seeding failed: {e}")
        db.session.rollback()
        raise

# Usage
if __name__ == "__main__":
    run_all_seeds()
```

### **8. Environment-Specific Seeds**
```python
# seeds/environment_specific.py
def seed_development():
    """Seed data for development environment"""
    # More test data for development
    seed_test_users(100)  # 100 test users
    seed_test_products(50)  # 50 test products
    seed_test_orders(200)  # 200 test orders

def seed_production():
    """Seed data for production environment"""
    # Only essential data for production
    seed_reference_data()
    seed_user_roles()
    seed_admin_user()  # Only admin user
    seed_configuration()

def seed_testing():
    """Seed data for testing environment"""
    # Minimal data for testing
    seed_reference_data()
    seed_user_roles()
    seed_test_users(10)  # 10 test users
    seed_test_products(20)  # 20 test products
```

This comprehensive guide covers all aspects of database migrations, from basic concepts to advanced practices, including practical examples and best practices for maintaining data integrity and testing migrations.
