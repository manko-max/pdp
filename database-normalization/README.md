# Database Normalization

## What is the primary purpose of database normalization?

**Database normalization** is the process of organizing data in a database to eliminate redundancy and improve data integrity. The primary purpose is to:

### **1. Eliminate Data Redundancy**
- Remove duplicate data across tables
- Reduce storage space requirements
- Prevent data inconsistency

### **2. Improve Data Integrity**
- Ensure data accuracy and consistency
- Prevent update anomalies
- Maintain referential integrity

### **3. Reduce Update Anomalies**
- **Insertion Anomalies**: Problems when inserting new data
- **Update Anomalies**: Problems when updating existing data
- **Deletion Anomalies**: Problems when deleting data

### **4. Optimize Database Design**
- Create logical, well-structured tables
- Improve query performance
- Simplify maintenance

## Describe the first normal form (1NF). What does it mean for data to be "atomic"?

### **First Normal Form (1NF) Requirements:**

#### **1. Atomic Values**
- Each cell must contain only one value
- No repeating groups or arrays
- No composite values that can be broken down

#### **2. Unique Column Names**
- Each column must have a unique name
- No duplicate column names

#### **3. Consistent Data Types**
- All values in a column must be of the same data type
- No mixed data types in a single column

### **What does "atomic" mean?**

**Atomic** means that a value cannot be further divided into smaller meaningful parts. It's the smallest unit of data that has meaning in the context of the database.

### **Examples:**

#### **❌ NOT in 1NF (Non-atomic values):**
```sql
-- BAD: Non-atomic values
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100),
    subjects VARCHAR(200)  -- "Math, Physics, Chemistry" - not atomic!
);

-- Data example:
INSERT INTO students VALUES 
(1, 'John Doe', 'Math, Physics, Chemistry'),
(2, 'Jane Smith', 'Math, Biology, History');
```

#### **✅ In 1NF (Atomic values):**
```sql
-- GOOD: Atomic values
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE student_subjects (
    student_id INT,
    subject_name VARCHAR(50),
    PRIMARY KEY (student_id, subject_name),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Data example:
INSERT INTO students VALUES 
(1, 'John Doe'),
(2, 'Jane Smith');

INSERT INTO student_subjects VALUES 
(1, 'Math'),
(1, 'Physics'),
(1, 'Chemistry'),
(2, 'Math'),
(2, 'Biology'),
(2, 'History');
```

#### **❌ NOT in 1NF (Repeating groups):**
```sql
-- BAD: Repeating groups
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    product1 VARCHAR(100),
    quantity1 INT,
    product2 VARCHAR(100),
    quantity2 INT,
    product3 VARCHAR(100),
    quantity3 INT
);
```

#### **✅ In 1NF (No repeating groups):**
```sql
-- GOOD: No repeating groups
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INT,
    product_name VARCHAR(100),
    quantity INT,
    PRIMARY KEY (order_id, product_name),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

## What is the requirement for a table to be in the second normal form (2NF)?

### **Second Normal Form (2NF) Requirements:**

#### **1. Must be in 1NF**
- All 1NF requirements must be satisfied

#### **2. No Partial Dependencies**
- All non-key attributes must be fully functionally dependent on the primary key
- No non-key attribute should depend on only part of a composite primary key

### **What is a Partial Dependency?**

A **partial dependency** occurs when a non-key attribute depends on only part of a composite primary key, not the entire key.

### **Examples:**

#### **❌ NOT in 2NF (Partial dependency):**
```sql
-- BAD: Partial dependency
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id, not on (order_id, product_id)
    quantity INT,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id)
);

-- Problem: product_name depends only on product_id, not on the full primary key
-- If we know product_id, we know product_name, regardless of order_id
```

#### **✅ In 2NF (No partial dependencies):**
```sql
-- GOOD: No partial dependencies
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    order_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    unit_price DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### **Step-by-step 2NF Process:**

#### **Step 1: Identify the Primary Key**
```sql
-- Original table with composite primary key
CREATE TABLE student_courses (
    student_id INT,
    course_id INT,
    student_name VARCHAR(100),    -- Depends on student_id only
    course_name VARCHAR(100),     -- Depends on course_id only
    grade CHAR(1),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

#### **Step 2: Identify Partial Dependencies**
- `student_name` depends only on `student_id` (partial dependency)
- `course_name` depends only on `course_id` (partial dependency)
- `grade` and `enrollment_date` depend on the full primary key

#### **Step 3: Create Separate Tables**
```sql
-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

-- Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

-- Student courses table (2NF)
CREATE TABLE student_courses (
    student_id INT,
    course_id INT,
    grade CHAR(1),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## What is a transitive dependency and how does it relate to the third normal form (3NF)?

### **Transitive Dependency Definition:**

A **transitive dependency** occurs when a non-key attribute depends on another non-key attribute, rather than directly on the primary key.

**Pattern**: A → B → C (where A is the primary key, B is a non-key attribute, and C depends on B)

### **Third Normal Form (3NF) Requirements:**

#### **1. Must be in 2NF**
- All 2NF requirements must be satisfied

#### **2. No Transitive Dependencies**
- All non-key attributes must be directly dependent on the primary key
- No non-key attribute should depend on another non-key attribute

### **Examples:**

#### **❌ NOT in 3NF (Transitive dependency):**
```sql
-- BAD: Transitive dependency
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department_id INT,
    department_name VARCHAR(100),  -- Depends on department_id, not on employee_id
    department_location VARCHAR(100)  -- Depends on department_id, not on employee_id
);

-- Transitive dependency: employee_id → department_id → department_name
-- If we know department_id, we know department_name, regardless of employee_id
```

#### **✅ In 3NF (No transitive dependencies):**
```sql
-- GOOD: No transitive dependencies
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    department_location VARCHAR(100)
);
```

### **Step-by-step 3NF Process:**

#### **Step 1: Identify Transitive Dependencies**
```sql
-- Original table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),    -- Depends on customer_id, not on order_id
    customer_email VARCHAR(100),   -- Depends on customer_id, not on order_id
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Transitive dependency: order_id → customer_id → customer_name
```

#### **Step 2: Create Separate Tables**
```sql
-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100)
);

-- Orders table (3NF)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

### **Real-world Example:**

#### **❌ NOT in 3NF:**
```sql
CREATE TABLE student_enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    student_name VARCHAR(100),     -- Transitive: depends on student_id
    student_major VARCHAR(100),    -- Transitive: depends on student_id
    course_id INT,
    course_name VARCHAR(100),      -- Transitive: depends on course_id
    course_credits INT,            -- Transitive: depends on course_id
    grade CHAR(1),
    enrollment_date DATE
);
```

#### **✅ In 3NF:**
```sql
-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100),
    student_major VARCHAR(100)
);

-- Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100),
    course_credits INT
);

-- Student enrollments table (3NF)
CREATE TABLE student_enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    grade CHAR(1),
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## How does the Boyce-Codd Normal Form (BCNF) differ from the Third Normal Form (3NF)?

### **Boyce-Codd Normal Form (BCNF) Requirements:**

#### **1. Must be in 3NF**
- All 3NF requirements must be satisfied

#### **2. No Overlapping Candidate Keys**
- Every determinant must be a candidate key
- No non-key attribute can determine another non-key attribute

### **Key Difference:**

- **3NF**: Allows non-key attributes to determine other non-key attributes, as long as the determining attribute is part of a candidate key
- **BCNF**: Requires that every determinant must be a candidate key

### **Examples:**

#### **❌ In 3NF but NOT in BCNF:**
```sql
-- Example: Student-Course-Instructor relationship
CREATE TABLE student_course_instructor (
    student_id INT,
    course_id INT,
    instructor_id INT,
    instructor_name VARCHAR(100),  -- Depends on instructor_id
    PRIMARY KEY (student_id, course_id)
);

-- This is in 3NF because:
-- - No partial dependencies (instructor_name depends on instructor_id, which is part of the key)
-- - No transitive dependencies

-- But NOT in BCNF because:
-- - instructor_id determines instructor_name
-- - instructor_id is not a candidate key (it's not unique)
```

#### **✅ In BCNF:**
```sql
-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

-- Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

-- Instructors table
CREATE TABLE instructors (
    instructor_id INT PRIMARY KEY,
    instructor_name VARCHAR(100)
);

-- Student course instructor table (BCNF)
CREATE TABLE student_course_instructor (
    student_id INT,
    course_id INT,
    instructor_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);
```

### **Another BCNF Example:**

#### **❌ In 3NF but NOT in BCNF:**
```sql
-- Example: Employee-Department-Manager relationship
CREATE TABLE employee_department (
    employee_id INT,
    department_id INT,
    manager_id INT,
    manager_name VARCHAR(100),  -- Depends on manager_id
    PRIMARY KEY (employee_id, department_id)
);

-- Problem: manager_id determines manager_name, but manager_id is not a candidate key
```

#### **✅ In BCNF:**
```sql
-- Employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100)
);

-- Departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- Managers table
CREATE TABLE managers (
    manager_id INT PRIMARY KEY,
    manager_name VARCHAR(100)
);

-- Employee department table (BCNF)
CREATE TABLE employee_department (
    employee_id INT,
    department_id INT,
    manager_id INT,
    PRIMARY KEY (employee_id, department_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES managers(manager_id)
);
```

## Can you give an example of a situation where it might not be desirable to fully normalize a database?

### **When Denormalization is Beneficial:**

#### **1. Performance-Critical Applications**
```sql
-- HIGHLY NORMALIZED (3NF/BCNF)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20)
);

-- Query to get order with customer info
SELECT o.order_id, o.order_date, o.total_amount, c.customer_name, c.customer_email
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_id = 123;

-- DENORMALIZED for performance
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),    -- Denormalized
    customer_email VARCHAR(100),   -- Denormalized
    order_date DATE,
    total_amount DECIMAL(10,2)
);

-- Query to get order with customer info
SELECT order_id, order_date, total_amount, customer_name, customer_email
FROM orders
WHERE order_id = 123;
```

#### **2. Reporting and Analytics**
```sql
-- HIGHLY NORMALIZED
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

-- Complex query for reporting
SELECT c.category_name, p.product_name, SUM(s.quantity * s.unit_price) as total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY c.category_name, p.product_name
ORDER BY total_sales DESC;

-- DENORMALIZED for reporting
CREATE TABLE sales_summary (
    sale_id INT PRIMARY KEY,
    product_name VARCHAR(100),     -- Denormalized
    category_name VARCHAR(100),    -- Denormalized
    customer_name VARCHAR(100),    -- Denormalized
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)     -- Denormalized
);

-- Simple query for reporting
SELECT category_name, product_name, SUM(total_amount) as total_sales
FROM sales_summary
WHERE sale_date >= '2024-01-01'
GROUP BY category_name, product_name
ORDER BY total_sales DESC;
```

#### **3. Real-time Systems**
```sql
-- HIGHLY NORMALIZED
CREATE TABLE user_sessions (
    session_id INT PRIMARY KEY,
    user_id INT,
    login_time TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    last_login TIMESTAMP
);

-- DENORMALIZED for real-time access
CREATE TABLE user_sessions (
    session_id INT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),          -- Denormalized
    email VARCHAR(100),            -- Denormalized
    login_time TIMESTAMP,
    last_login TIMESTAMP           -- Denormalized
);
```

#### **4. Data Warehousing**
```sql
-- HIGHLY NORMALIZED (OLTP)
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- DENORMALIZED (OLAP/Data Warehouse)
CREATE TABLE fact_sales (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),     -- Denormalized
    product_category VARCHAR(100), -- Denormalized
    customer_id INT,
    customer_name VARCHAR(100),    -- Denormalized
    customer_region VARCHAR(100),  -- Denormalized
    order_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)     -- Denormalized
);
```

### **When to Denormalize:**

#### **1. Read-Heavy Workloads**
- Reporting systems
- Analytics platforms
- Data warehouses
- Search systems

#### **2. Performance Requirements**
- Real-time systems
- High-traffic applications
- Mobile applications
- IoT systems

#### **3. Simplified Queries**
- Business intelligence tools
- Dashboard applications
- API responses
- Caching systems

## What are some potential disadvantages or challenges of database normalization?

### **1. Performance Issues**

#### **Query Complexity**
```sql
-- NORMALIZED: Complex joins required
SELECT o.order_id, o.order_date, o.total_amount,
       c.customer_name, c.customer_email,
       p.product_name, p.product_category,
       s.supplier_name, s.supplier_contact
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE o.order_date >= '2024-01-01';

-- DENORMALIZED: Simple query
SELECT order_id, order_date, total_amount,
       customer_name, customer_email,
       product_name, product_category,
       supplier_name, supplier_contact
FROM order_summary
WHERE order_date >= '2024-01-01';
```

#### **Join Overhead**
```sql
-- Performance impact of multiple joins
EXPLAIN ANALYZE
SELECT o.order_id, c.customer_name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- Result: Multiple table scans, index lookups, and join operations
-- Cost: High CPU and I/O usage
```

### **2. Storage Overhead**

#### **Additional Tables**
```sql
-- NORMALIZED: Multiple tables
CREATE TABLE customers (customer_id INT PRIMARY KEY, customer_name VARCHAR(100));
CREATE TABLE orders (order_id INT PRIMARY KEY, customer_id INT);
CREATE TABLE products (product_id INT PRIMARY KEY, product_name VARCHAR(100));
CREATE TABLE order_items (order_id INT, product_id INT, quantity INT);

-- Storage: 4 tables + foreign key constraints + indexes

-- DENORMALIZED: Single table
CREATE TABLE order_summary (
    order_id INT,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INT
);

-- Storage: 1 table + indexes
```

#### **Foreign Key Constraints**
```sql
-- NORMALIZED: Foreign key overhead
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Storage overhead:
-- - Foreign key constraint metadata
-- - Index on customer_id
-- - Referential integrity checks
```

### **3. Maintenance Complexity**

#### **Update Anomalies**
```sql
-- NORMALIZED: Update in multiple places
UPDATE customers 
SET customer_name = 'New Name' 
WHERE customer_id = 123;

-- Must also update:
-- - All orders referencing this customer
-- - All related tables
-- - All cached data
-- - All application code
```

#### **Schema Changes**
```sql
-- NORMALIZED: Schema change affects multiple tables
ALTER TABLE customers ADD COLUMN customer_phone VARCHAR(20);

-- Must also consider:
-- - Impact on orders table
-- - Impact on order_items table
-- - Impact on all related tables
-- - Impact on all queries
-- - Impact on all applications
```

### **4. Development Complexity**

#### **Complex Queries**
```sql
-- NORMALIZED: Complex query for simple business logic
SELECT 
    c.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(oi.quantity * p.unit_price) as total_spent,
    AVG(oi.quantity * p.unit_price) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE c.customer_id = 123
GROUP BY c.customer_name;

-- DENORMALIZED: Simple query
SELECT 
    customer_name,
    total_orders,
    total_spent,
    avg_order_value
FROM customer_summary
WHERE customer_id = 123;
```

#### **Application Code Complexity**
```python
# NORMALIZED: Complex application code
def get_customer_orders(customer_id):
    # Query customers table
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    
    # Query orders table
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    
    # Query order items for each order
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item.product = product
        order.items = order_items
    
    return customer, orders

# DENORMALIZED: Simple application code
def get_customer_orders(customer_id):
    return db.query(CustomerSummary).filter(CustomerSummary.customer_id == customer_id).first()
```

### **5. Caching Challenges**

#### **Cache Invalidation**
```sql
-- NORMALIZED: Cache invalidation complexity
UPDATE customers SET customer_name = 'New Name' WHERE customer_id = 123;

-- Must invalidate:
-- - Customer cache
-- - Order cache (if it includes customer name)
-- - Order items cache
-- - Product cache (if it includes customer info)
-- - All related caches
```

### **6. Backup and Recovery**

#### **Referential Integrity**
```sql
-- NORMALIZED: Backup complexity
-- Must backup in correct order to maintain referential integrity
-- 1. Backup customers table
-- 2. Backup orders table
-- 3. Backup order_items table
-- 4. Backup products table

-- DENORMALIZED: Simple backup
-- Can backup single table without dependency issues
```

### **7. Testing Complexity**

#### **Test Data Setup**
```python
# NORMALIZED: Complex test data setup
def setup_test_data():
    # Create customer
    customer = Customer(name="Test Customer", email="test@example.com")
    db.add(customer)
    db.commit()
    
    # Create product
    product = Product(name="Test Product", price=10.00)
    db.add(product)
    db.commit()
    
    # Create order
    order = Order(customer_id=customer.id, order_date=datetime.now())
    db.add(order)
    db.commit()
    
    # Create order item
    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=2)
    db.add(order_item)
    db.commit()

# DENORMALIZED: Simple test data setup
def setup_test_data():
    order_summary = OrderSummary(
        customer_name="Test Customer",
        product_name="Test Product",
        quantity=2,
        total_amount=20.00
    )
    db.add(order_summary)
    db.commit()
```

### **8. Migration Complexity**

#### **Schema Evolution**
```sql
-- NORMALIZED: Complex migration
-- Adding a new field requires changes to multiple tables
ALTER TABLE customers ADD COLUMN customer_phone VARCHAR(20);
ALTER TABLE orders ADD COLUMN customer_phone VARCHAR(20);  -- If denormalized
ALTER TABLE order_items ADD COLUMN customer_phone VARCHAR(20);  -- If denormalized

-- Must update all related tables and maintain consistency
```

### **9. Memory Usage**

#### **Join Operations**
```sql
-- NORMALIZED: High memory usage for joins
SELECT o.order_id, c.customer_name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;

-- Memory usage:
-- - Temporary join tables
-- - Index lookups
-- - Sort operations
-- - Hash tables for joins
```

### **10. Network Overhead**

#### **Multiple Round Trips**
```python
# NORMALIZED: Multiple database round trips
def get_customer_info(customer_id):
    # Round trip 1: Get customer
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    
    # Round trip 2: Get orders
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    
    # Round trip 3: Get order items for each order
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        order.items = order_items
    
    return customer, orders

# DENORMALIZED: Single round trip
def get_customer_info(customer_id):
    return db.query(CustomerSummary).filter(CustomerSummary.customer_id == customer_id).first()
```

### **Summary of Disadvantages:**

1. **Performance**: Complex queries, multiple joins, high CPU usage
2. **Storage**: Additional tables, foreign key constraints, indexes
3. **Maintenance**: Update anomalies, schema changes, referential integrity
4. **Development**: Complex queries, application code, testing
5. **Caching**: Cache invalidation complexity
6. **Backup**: Referential integrity constraints
7. **Testing**: Complex test data setup
8. **Migration**: Schema evolution complexity
9. **Memory**: High memory usage for joins
10. **Network**: Multiple database round trips

### **When to Consider Denormalization:**

- **Read-heavy workloads** (reporting, analytics)
- **Performance-critical applications** (real-time systems)
- **Simple query requirements** (APIs, dashboards)
- **Limited storage constraints** (embedded systems)
- **Development time constraints** (prototypes, MVPs)

The key is to find the right balance between normalization and denormalization based on your specific use case, performance requirements, and maintenance capabilities.
