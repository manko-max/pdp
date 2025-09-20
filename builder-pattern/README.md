# Builder Pattern

## Table of Contents
1. [Overview](#overview)
2. [Definition](#definition)
3. [Builder vs Factory Pattern](#builder-vs-factory-pattern)
4. [Real-World Scenarios](#real-world-scenarios)
5. [Key Components](#key-components)
6. [Advantages and Drawbacks](#advantages-and-drawbacks)
7. [When to Use](#when-to-use)
8. [When NOT to Use](#when-not-to-use)
9. [Step-by-Step Construction](#step-by-step-construction)
10. [Code Readability and Flexibility](#code-readability-and-flexibility)
11. [Different Representations](#different-representations)
12. [Implementation Example](#implementation-example)
13. [Best Practices](#best-practices)
14. [Common Variations](#common-variations)

## Overview

The Builder pattern is a creational design pattern that allows you to construct complex objects step by step. It separates the construction of a complex object from its representation, enabling the same construction process to create different representations.

## Definition

**Builder Pattern**: A design pattern that provides a way to construct complex objects step by step. It allows you to produce different types and representations of an object using the same construction code.

### Key Characteristics:
- **Step-by-step construction**: Objects are built incrementally
- **Fluent interface**: Methods return the builder instance for chaining
- **Separation of concerns**: Construction logic is separate from the product
- **Flexibility**: Same process can create different representations

## Builder vs Factory Pattern

| Aspect | Builder Pattern | Factory Pattern |
|--------|----------------|-----------------|
| **Purpose** | Construct complex objects step by step | Create objects without specifying exact class |
| **Construction** | Incremental, configurable | Immediate, fixed |
| **Flexibility** | High - can customize each step | Low - predefined creation |
| **Complexity** | Good for complex objects | Good for simple objects |
| **Parameters** | Many optional parameters | Few or no parameters |
| **Use Case** | When object has many parts | When object creation is straightforward |

### Example Comparison:

**Factory Pattern:**
```python
# Simple, immediate creation
car = CarFactory.create_sports_car()
```

**Builder Pattern:**
```python
# Step-by-step, configurable creation
car = (CarBuilder()
       .set_engine("V8")
       .set_color("Red")
       .set_transmission("Manual")
       .add_feature("GPS")
       .add_feature("Leather Seats")
       .build())
```

## Real-World Scenarios

### 1. Database Query Builder
```python
query = (QueryBuilder()
         .select("name", "email")
         .from_table("users")
         .where("age > 18")
         .order_by("name")
         .limit(10)
         .build())
```

### 2. HTTP Request Builder
```python
request = (HttpRequestBuilder()
           .set_method("POST")
           .set_url("https://api.example.com/users")
           .add_header("Content-Type", "application/json")
           .add_header("Authorization", "Bearer token")
           .set_body({"name": "John", "email": "john@example.com"})
           .build())
```

### 3. Configuration Builder
```python
config = (ConfigBuilder()
          .set_database_url("postgresql://localhost:5432/mydb")
          .set_redis_url("redis://localhost:6379")
          .set_debug_mode(True)
          .add_middleware("cors")
          .add_middleware("logging")
          .build())
```

### 4. Document Builder (PDF, Word)
```python
document = (DocumentBuilder()
            .add_title("Project Report")
            .add_author("John Doe")
            .add_section("Introduction")
            .add_paragraph("This is the introduction...")
            .add_section("Conclusion")
            .add_paragraph("This is the conclusion...")
            .build())
```

## Key Components

### 1. Product
The complex object being constructed.

```python
class Product:
    def __init__(self):
        self.part_a = None
        self.part_b = None
        self.part_c = None
```

### 2. Builder Interface
Defines the construction steps.

```python
from abc import ABC, abstractmethod

class Builder(ABC):
    @abstractmethod
    def build_part_a(self) -> 'Builder':
        pass
    
    @abstractmethod
    def build_part_b(self) -> 'Builder':
        pass
    
    @abstractmethod
    def build_part_c(self) -> 'Builder':
        pass
    
    @abstractmethod
    def build(self) -> Product:
        pass
```

### 3. Concrete Builder
Implements the construction steps for a specific product variant.

```python
class ConcreteBuilder(Builder):
    def __init__(self):
        self.product = Product()
    
    def build_part_a(self) -> 'Builder':
        self.product.part_a = "Specific Part A"
        return self
    
    def build_part_b(self) -> 'Builder':
        self.product.part_b = "Specific Part B"
        return self
    
    def build_part_c(self) -> 'Builder':
        self.product.part_c = "Specific Part C"
        return self
    
    def build(self) -> Product:
        return self.product
```

### 4. Director (Optional)
Orchestrates the construction process.

```python
class Director:
    def __init__(self, builder: Builder):
        self.builder = builder
    
    def construct(self) -> Product:
        return (self.builder
                .build_part_a()
                .build_part_b()
                .build_part_c()
                .build())
```

## Advantages and Drawbacks

### Advantages

#### 1. **Step-by-Step Construction**
- Objects are built incrementally
- Each step can be validated
- Construction can be paused and resumed

#### 2. **Flexibility**
- Same construction process for different representations
- Easy to add new product variants
- Optional parameters can be handled gracefully

#### 3. **Readability**
- Fluent interface makes code self-documenting
- Method chaining is intuitive
- Construction logic is clear and organized

#### 4. **Reusability**
- Construction code can be reused
- Common construction patterns can be extracted
- Easy to create different configurations

#### 5. **Separation of Concerns**
- Construction logic is separate from product
- Product class remains simple
- Easy to modify construction without affecting product

### Drawbacks

#### 1. **Complexity**
- More classes and interfaces
- Can be overkill for simple objects
- Steeper learning curve

#### 2. **Performance**
- Additional object creation overhead
- Method chaining can create temporary objects
- More memory usage during construction

#### 3. **Verbosity**
- More code to write and maintain
- Can be verbose for simple use cases
- Requires discipline to maintain consistency

#### 4. **Debugging**
- Harder to debug method chains
- Error messages can be less clear
- Stack traces can be complex

## When to Use

### ✅ Use Builder Pattern When:

1. **Complex Object Construction**
   - Object has many parts or parameters
   - Construction process is multi-step
   - Different combinations of parts are needed

2. **Optional Parameters**
   - Many optional configuration options
   - Need to handle different parameter combinations
   - Want to avoid parameter explosion

3. **Different Representations**
   - Same construction process for different products
   - Need to create variations of the same object
   - Want to reuse construction logic

4. **Fluent Interface**
   - Want readable, chainable method calls
   - Need self-documenting code
   - Want to improve developer experience

5. **Validation During Construction**
   - Need to validate each step
   - Want to ensure object consistency
   - Need to handle construction errors gracefully

### Example Use Cases:
- Database query builders
- HTTP request/response builders
- Configuration builders
- Document builders
- Test data builders
- API client builders

## When NOT to Use

### ❌ Avoid Builder Pattern When:

1. **Simple Objects**
   - Object has few parameters
   - Construction is straightforward
   - No need for step-by-step building

2. **Performance Critical**
   - Construction happens frequently
   - Memory usage is a concern
   - Need maximum performance

3. **Immutable Objects**
   - Object should be created atomically
   - No need for incremental construction
   - Want to ensure object consistency

4. **Single Representation**
   - Only one way to create the object
   - No variations needed
   - Construction process is fixed

### Example Anti-Patterns:
```python
# Don't use Builder for simple objects
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# This is overkill
point = PointBuilder().set_x(10).set_y(20).build()
# This is better
point = Point(10, 20)
```

## Step-by-Step Construction

The Builder pattern enables step-by-step construction by:

### 1. **Incremental Building**
```python
builder = CarBuilder()
builder.set_engine("V8")      # Step 1
builder.set_color("Red")      # Step 2
builder.add_wheels(4)         # Step 3
builder.add_features(["GPS", "AC"])  # Step 4
car = builder.build()         # Final step
```

### 2. **Validation at Each Step**
```python
def set_engine(self, engine_type: str) -> 'CarBuilder':
    if engine_type not in ["V4", "V6", "V8"]:
        raise ValueError(f"Invalid engine type: {engine_type}")
    self.car.engine = engine_type
    return self
```

### 3. **Conditional Construction**
```python
def build(self) -> Car:
    if not self.car.engine:
        raise ValueError("Engine is required")
    if not self.car.wheels:
        self.car.wheels = 4  # Default value
    return self.car
```

### 4. **Resumable Construction**
```python
# Can pause and resume construction
builder = CarBuilder()
builder.set_engine("V8")
# ... some time later ...
builder.set_color("Red").build()
```

## Code Readability and Flexibility

### 1. **Fluent Interface**
```python
# Readable method chaining
query = (QueryBuilder()
         .select("name", "email")
         .from_table("users")
         .where("age > 18")
         .order_by("name")
         .build())
```

### 2. **Self-Documenting Code**
```python
# Code tells a story
email = (EmailBuilder()
         .to("user@example.com")
         .from_("noreply@company.com")
         .subject("Welcome!")
         .body("Welcome to our service!")
         .add_attachment("welcome.pdf")
         .build())
```

### 3. **Flexible Configuration**
```python
# Easy to create different configurations
basic_config = ConfigBuilder().set_database_url("...").build()
advanced_config = (ConfigBuilder()
                   .set_database_url("...")
                   .set_redis_url("...")
                   .set_debug_mode(True)
                   .add_middleware("cors")
                   .build())
```

### 4. **Method Chaining Benefits**
- **Readability**: Code flows naturally
- **Discoverability**: IDE can suggest next methods
- **Consistency**: Same pattern throughout codebase
- **Maintainability**: Easy to add/remove steps

## Different Representations

The Builder pattern allows the same construction process to create different representations:

### 1. **Multiple Concrete Builders**
```python
# Same interface, different implementations
burger_builder = BurgerMealBuilder()
pizza_builder = PizzaMealBuilder()
salad_builder = SaladMealBuilder()

# Same construction process
burger_meal = director.construct_meal(burger_builder)
pizza_meal = director.construct_meal(pizza_builder)
salad_meal = director.construct_meal(salad_builder)
```

### 2. **Configurable Builders**
```python
class DatabaseBuilder:
    def __init__(self):
        self.db_type = None
        self.host = None
        self.port = None
    
    def set_type(self, db_type: str) -> 'DatabaseBuilder':
        self.db_type = db_type
        return self
    
    def build(self) -> Database:
        if self.db_type == "postgresql":
            return PostgreSQLDatabase(self.host, self.port)
        elif self.db_type == "mysql":
            return MySQLDatabase(self.host, self.port)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
```

### 3. **Template Method Pattern Integration**
```python
class AbstractCarBuilder:
    def build_car(self) -> Car:
        car = Car()
        self.build_engine(car)
        self.build_wheels(car)
        self.build_interior(car)
        return car
    
    @abstractmethod
    def build_engine(self, car: Car):
        pass
    
    @abstractmethod
    def build_wheels(self, car: Car):
        pass
    
    @abstractmethod
    def build_interior(self, car: Car):
        pass

class SportsCarBuilder(AbstractCarBuilder):
    def build_engine(self, car: Car):
        car.engine = "V8 Turbo"
    
    def build_wheels(self, car: Car):
        car.wheels = "Racing Wheels"
    
    def build_interior(self, car: Car):
        car.interior = "Leather Racing Seats"
```

## Implementation Example

See `meal_builder.py` for a complete implementation example of the Builder pattern in a restaurant meal ordering system.

### Key Features of the Example:
- **Product**: `Meal` class with main course, side, and drink
- **Builder Interface**: `MealBuilder` with abstract methods
- **Concrete Builders**: `BurgerMealBuilder`, `PizzaMealBuilder`, `SaladMealBuilder`
- **Director**: `MealDirector` that orchestrates construction
- **Fluent Interface**: Method chaining for readable code

### Running the Example:
```bash
python3 meal_builder.py
```

## Best Practices

### 1. **Method Chaining**
- Always return `self` from builder methods
- Use type hints for better IDE support
- Keep method names descriptive

### 2. **Validation**
- Validate parameters at each step
- Provide clear error messages
- Fail fast on invalid input

### 3. **Default Values**
- Provide sensible defaults where appropriate
- Document default behavior
- Allow overriding of defaults

### 4. **Immutability**
- Consider making the final product immutable
- Use `build()` method to finalize construction
- Prevent modification after building

### 5. **Error Handling**
- Handle construction errors gracefully
- Provide meaningful error messages
- Consider partial construction scenarios

### 6. **Documentation**
- Document the construction process
- Provide usage examples
- Explain the purpose of each step

## Common Variations

### 1. **Fluent Builder**
```python
class FluentBuilder:
    def with_name(self, name: str) -> 'FluentBuilder':
        self.name = name
        return self
    
    def with_age(self, age: int) -> 'FluentBuilder':
        self.age = age
        return self
```

### 2. **Step Builder**
```python
class StepBuilder:
    def step1(self) -> 'Step1Builder':
        return Step1Builder(self)
    
    def step2(self) -> 'Step2Builder':
        return Step2Builder(self)

class Step1Builder:
    def __init__(self, parent):
        self.parent = parent
    
    def set_name(self, name: str) -> 'Step2Builder':
        self.parent.name = name
        return Step2Builder(self.parent)
```

### 3. **Generic Builder**
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class GenericBuilder(Generic[T]):
    def __init__(self, product_class: type):
        self.product_class = product_class
        self.product = product_class()
    
    def build(self) -> T:
        return self.product
```

### 4. **Builder with Validation**
```python
class ValidatingBuilder:
    def __init__(self):
        self.validation_errors = []
    
    def validate(self) -> bool:
        if not self.name:
            self.validation_errors.append("Name is required")
        return len(self.validation_errors) == 0
    
    def build(self) -> Product:
        if not self.validate():
            raise ValueError(f"Validation failed: {self.validation_errors}")
        return self.product
```

## Conclusion

The Builder pattern is a powerful tool for constructing complex objects step by step. It provides flexibility, readability, and maintainability when dealing with objects that have many parts or optional parameters. While it adds some complexity, the benefits often outweigh the costs in scenarios where object construction is complex or needs to be highly configurable.

Key takeaways:
- Use for complex objects with many parts
- Provides step-by-step construction
- Enables different representations with same process
- Improves code readability through fluent interface
- Separates construction logic from product representation
- Consider performance implications for simple objects
