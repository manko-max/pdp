# Entity-Relationship (ER) Notation

## What is an Entity in ER notation and how is it represented in an ER diagram?

### **Entity Definition:**

An **Entity** is a real-world object, concept, or thing that can be distinctly identified and about which data can be stored. It represents a class of objects with similar characteristics.

### **Entity Characteristics:**
- **Distinct Identity**: Each entity instance must be uniquely identifiable
- **Attributes**: Entities have properties or characteristics
- **Instances**: An entity can have multiple instances (records)
- **Independence**: Entities exist independently of other entities

### **Entity Representation in ER Diagrams:**

#### **1. Rectangle Symbol**
```
┌─────────────┐
│   Entity    │
└─────────────┘
```

#### **2. Examples of Entities:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Student   │    │   Course    │    │  Professor  │
└─────────────┘    └─────────────┘    └─────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Customer  │    │    Order    │    │   Product   │
└─────────────┘    └─────────────┘    └─────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Employee  │    │ Department  │    │   Project   │
└─────────────┘    └─────────────┘    └─────────────┘
```

#### **3. Entity Types:**
- **Strong Entity**: Has its own primary key
- **Weak Entity**: Depends on another entity for identification

```
┌─────────────┐    ┌─────────────┐
│   Student   │    │  Dependent  │
│ (Strong)    │    │  (Weak)     │
└─────────────┘    └─────────────┘
```

## Can you explain what an Attribute is in the context of ER notation?

### **Attribute Definition:**

An **Attribute** is a property or characteristic of an entity that describes it. Attributes provide detailed information about entities.

### **Attribute Types:**

#### **1. Simple vs Composite Attributes**
```
Simple Attribute:     Composite Attribute:
┌─────────────┐       ┌─────────────┐
│   Student   │       │   Student   │
│             │       │             │
│ student_id  │       │    name     │
│ student_age │       │   ┌─────┐   │
│ student_gpa │       │   │first│   │
└─────────────┘       │   │last │   │
                      │   └─────┘   │
                      └─────────────┘
```

#### **2. Single-valued vs Multi-valued Attributes**
```
Single-valued:        Multi-valued:
┌─────────────┐       ┌─────────────┐
│   Student   │       │   Student   │
│             │       │             │
│ student_id  │       │ student_id  │
│ student_age │       │ student_age │
│ student_gpa │       │   {phone}   │
└─────────────┘       └─────────────┘
```

#### **3. Stored vs Derived Attributes**
```
Stored Attribute:     Derived Attribute:
┌─────────────┐       ┌─────────────┐
│   Student   │       │   Student   │
│             │       │             │
│ student_id  │       │ student_id  │
│ birth_date  │       │ birth_date  │
│ student_age │       │ student_age │
└─────────────┘       └─────────────┘
                      (derived from birth_date)
```

#### **4. Key Attributes**
```
┌─────────────┐
│   Student   │
│             │
│ student_id  │ ← Primary Key (underlined)
│ student_name│
│ student_gpa │
└─────────────┘
```

### **Attribute Notation Examples:**

#### **Complete Entity with Attributes:**
```
┌─────────────────────────┐
│        Student          │
│                         │
│ student_id (PK)         │
│ student_name            │
│ student_email           │
│ student_phone           │
│ student_gpa             │
│ enrollment_date         │
└─────────────────────────┘
```

#### **Entity with Different Attribute Types:**
```
┌─────────────────────────┐
│        Employee         │
│                         │
│ emp_id (PK)             │
│ emp_name                │
│   ├─ first_name         │
│   └─ last_name          │
│ emp_phone {multi}       │
│ emp_salary              │
│ emp_years_service       │ ← derived
└─────────────────────────┘
```

## How would you describe a Relationship in an ER diagram?

### **Relationship Definition:**

A **Relationship** is an association between two or more entities that describes how they are connected or related to each other.

### **Relationship Characteristics:**
- **Connects Entities**: Links two or more entities
- **Has a Name**: Describes the nature of the relationship
- **Has Cardinality**: Defines how many instances of one entity relate to instances of another entity
- **Can Have Attributes**: Relationships can have their own properties

### **Relationship Representation:**

#### **1. Diamond Symbol**
```
    ┌─────────────┐
    │ Relationship│
    └─────────────┘
```

#### **2. Basic Relationship Structure**
```
Entity A ──────┐
               │
               ├─┌─────────────┐─┐
               │ │ Relationship│ │
               ├─└─────────────┘─┤
               │
Entity B ──────┘
```

#### **3. Relationship Examples:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘

Customer ─────┐
              │
              ├─┌─────────────┐─┐
              │ │   Places    │ │
              ├─└─────────────┘─┤
              │
Order ────────┘

Employee ─────┐
              │
              ├─┌─────────────┐─┐
              │ │   Works     │ │
              ├─└─────────────┘─┤
              │
Department ───┘
```

#### **4. Relationship with Attributes:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              │ │             │ │
              │ │ grade       │ │
              │ │ date        │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
```

### **Relationship Types:**

#### **1. Binary Relationships (Two Entities)**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
```

#### **2. Ternary Relationships (Three Entities)**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Takes     │ │
              ├─└─────────────┘─┤
              │
Course ───────┼─┐
              │ │
              │ │
Professor ─────┘
```

#### **3. Recursive Relationships (Self-referencing)**
```
Employee ─────┐
              │
              ├─┌─────────────┐─┐
              │ │  Manages    │ │
              ├─└─────────────┘─┤
              │
Employee ─────┘
```

## In ER notation, what does a Double Rectangle represent?

### **Double Rectangle Definition:**

A **Double Rectangle** represents a **Weak Entity** in ER notation.

### **Weak Entity Characteristics:**
- **Dependent Entity**: Cannot exist without a strong entity
- **Partial Key**: Has a partial key (discriminator) but not a complete primary key
- **Identifying Relationship**: Connected to a strong entity through an identifying relationship
- **Double Diamond**: The relationship is represented with a double diamond

### **Weak Entity Representation:**

#### **1. Double Rectangle Symbol**
```
┌═════════════┐
│ Weak Entity │
└═════════════┘
```

#### **2. Complete Weak Entity Structure:**
```
Strong Entity ──────┐
                    │
                    ├─┌═════════════┐─┐
                    │ │Identifying  │ │
                    ├─└═════════════┘─┤
                    │
┌═════════════┐─────┘
│ Weak Entity │
│             │
│ partial_key │ ← Partial Key (dashed underline)
│ attribute1  │
│ attribute2  │
└═════════════┘
```

### **Weak Entity Examples:**

#### **1. Employee-Dependent Relationship:**
```
┌─────────────┐
│  Employee   │
│             │
│ emp_id (PK) │
│ emp_name    │
└─────────────┘
       │
       │
       ├─┌═════════════┐─┐
       │ │   Has       │ │
       ├─└═════════════┘─┤
       │
┌═════════════┐
│  Dependent  │
│             │
│ dep_name    │ ← Partial Key
│ dep_relation│
│ dep_age     │
└═════════════┘
```

#### **2. Course-Enrollment Relationship:**
```
┌─────────────┐
│   Course    │
│             │
│ course_id   │
│ course_name │
└─────────────┘
       │
       │
       ├─┌═════════════┐─┐
       │ │  Enrolls    │ │
       ├─└═════════════┘─┤
       │
┌═════════════┐
│ Enrollment  │
│             │
│ semester    │ ← Partial Key
│ year        │ ← Partial Key
│ grade       │
└═════════════┘
```

#### **3. Order-OrderItem Relationship:**
```
┌─────────────┐
│    Order    │
│             │
│ order_id    │
│ order_date  │
└─────────────┘
       │
       │
       ├─┌═════════════┐─┐
       │ │  Contains   │ │
       ├─└═════════════┘─┤
       │
┌═════════════┐
│ Order Item  │
│             │
│ item_seq    │ ← Partial Key
│ quantity    │
│ unit_price  │
└═════════════┘
```

### **Key Points about Weak Entities:**

#### **1. Identification Dependency:**
- Weak entities cannot be uniquely identified without their strong entity
- The combination of the strong entity's key and the weak entity's partial key forms the complete key

#### **2. Identifying Relationship:**
- The relationship between strong and weak entities is called an "identifying relationship"
- Represented with a double diamond
- The weak entity is always on the "many" side of the relationship

#### **3. Partial Key (Discriminator):**
- Weak entities have a partial key that, combined with the strong entity's key, forms the complete primary key
- Partial keys are represented with a dashed underline

## How would you represent a many-to-many relationship between two entities in an ER diagram?

### **Many-to-Many Relationship Definition:**

A **Many-to-Many (M:N) relationship** occurs when multiple instances of one entity can be associated with multiple instances of another entity.

### **Many-to-Many Representation:**

#### **1. Basic Many-to-Many Structure:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
```

#### **2. Cardinality Notation:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
      M                    N
```

#### **3. Crow's Foot Notation:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
      ││                    ││
      └┘                    └┘
```

### **Many-to-Many Examples:**

#### **1. Student-Course Enrollment:**
```
┌─────────────┐
│   Student   │
│             │
│ student_id  │
│ student_name│
└─────────────┘
       │
       │
       ├─┌─────────────┐─┐
       │ │   Enrolls   │ │
       ├─└─────────────┘─┤
       │
┌─────────────┐
│   Course    │
│             │
│ course_id   │
│ course_name │
└─────────────┘
```

#### **2. Employee-Project Assignment:**
```
┌─────────────┐
│  Employee   │
│             │
│ emp_id      │
│ emp_name    │
└─────────────┘
       │
       │
       ├─┌─────────────┐─┐
       │ │  Assigned   │ │
       ├─└─────────────┘─┤
       │
┌─────────────┐
│   Project   │
│             │
│ project_id  │
│ project_name│
└─────────────┘
```

#### **3. Customer-Product Purchase:**
```
┌─────────────┐
│  Customer   │
│             │
│ customer_id │
│ customer_name│
└─────────────┘
       │
       │
       ├─┌─────────────┐─┐
       │ │  Purchases  │ │
       ├─└─────────────┘─┤
       │
┌─────────────┐
│   Product   │
│             │
│ product_id  │
│ product_name│
└─────────────┘
```

### **Many-to-Many with Attributes:**

#### **1. Student-Course with Grade:**
```
┌─────────────┐
│   Student   │
│             │
│ student_id  │
│ student_name│
└─────────────┘
       │
       │
       ├─┌─────────────┐─┐
       │ │   Enrolls   │ │
       │ │             │ │
       │ │ grade       │ │
       │ │ date        │ │
       ├─└─────────────┘─┤
       │
┌─────────────┐
│   Course    │
│             │
│ course_id   │
│ course_name │
└─────────────┘
```

#### **2. Employee-Project with Role:**
```
┌─────────────┐
│  Employee   │
│             │
│ emp_id      │
│ emp_name    │
└─────────────┘
       │
       │
       ├─┌─────────────┐─┐
       │ │  Assigned   │ │
       │ │             │ │
       │ │ role        │ │
       │ │ start_date  │ │
       │ │ end_date    │ │
       ├─└─────────────┘─┤
       │
┌─────────────┐
│   Project   │
│             │
│ project_id  │
│ project_name│
└─────────────┘
```

### **Converting Many-to-Many to Relational Model:**

#### **1. Create Junction Table:**
```sql
-- Original Many-to-Many
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘

-- Converted to Relational Model
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    grade CHAR(1),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

#### **2. Junction Table with Attributes:**
```sql
-- Many-to-Many with Attributes
Employee ─────┐
              │
              ├─┌─────────────┐─┐
              │ │  Assigned   │ │
              │ │             │ │
              │ │ role        │ │
              │ │ start_date  │ │
              ├─└─────────────┘─┤
              │
Project ──────┘

-- Converted to Relational Model
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100)
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100)
);

CREATE TABLE assignments (
    emp_id INT,
    project_id INT,
    role VARCHAR(50),
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (emp_id, project_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
```

### **Cardinality Notation for Many-to-Many:**

#### **1. Chen Notation:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
      M                    N
```

#### **2. Crow's Foot Notation:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
      ││                    ││
      └┘                    └┘
```

#### **3. UML Notation:**
```
Student ──────┐
              │
              ├─┌─────────────┐─┐
              │ │   Enrolls   │ │
              ├─└─────────────┘─┤
              │
Course ───────┘
      *                    *
```

### **Key Points about Many-to-Many Relationships:**

#### **1. Bidirectional:**
- The relationship works in both directions
- A student can enroll in multiple courses
- A course can have multiple students

#### **2. Junction Table:**
- In the relational model, many-to-many relationships are implemented using junction tables
- Junction tables contain foreign keys to both related entities

#### **3. Attributes:**
- Many-to-many relationships can have their own attributes
- These attributes describe the relationship itself, not the entities

#### **4. Cardinality:**
- Always represented as M:N or *:*
- Both sides of the relationship can have multiple instances

This comprehensive guide covers all aspects of Entity-Relationship notation, from basic concepts to advanced relationships, with practical examples and clear explanations.
