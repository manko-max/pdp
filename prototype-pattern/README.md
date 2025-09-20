# Prototype Pattern

## Table of Contents
1. [Overview](#overview)
2. [Definition](#definition)
3. [Prototype vs Factory Pattern](#prototype-vs-factory-pattern)
4. [Real-World Examples](#real-world-examples)
5. [Key Components](#key-components)
6. [Advantages and Drawbacks](#advantages-and-drawbacks)
7. [When to Use](#when-to-use)
8. [When NOT to Use](#when-not-to-use)
9. [Costly Object Creation](#costly-object-creation)
10. [Runtime Object Management](#runtime-object-management)
11. [Composition over Inheritance](#composition-over-inheritance)
12. [Implementation Example](#implementation-example)
13. [Best Practices](#best-practices)
14. [Common Variations](#common-variations)

## Overview

The Prototype pattern is a creational design pattern that allows you to copy existing objects without making your code dependent on their classes. It's particularly useful when object creation is expensive and you need multiple similar instances.

## Definition

**Prototype Pattern**: A design pattern that creates objects by cloning existing instances (prototypes) rather than creating new ones from scratch. It specifies the kinds of objects to create using a prototypical instance and creates new objects by copying this prototype.

### Key Characteristics:
- **Cloning-based creation**: Objects are created by copying existing instances
- **Runtime flexibility**: New object types can be added at runtime
- **Performance optimization**: Avoids expensive initialization processes
- **Independence from classes**: Code doesn't depend on concrete classes

## Prototype vs Factory Pattern

| Aspect | Prototype Pattern | Factory Pattern |
|--------|------------------|-----------------|
| **Creation Method** | Cloning existing objects | Creating new objects from scratch |
| **Performance** | Fast (copying) | Can be slow (full initialization) |
| **Memory Usage** | Shared prototype data | Each object is independent |
| **Runtime Changes** | Easy to add/remove types | Harder to modify at runtime |
| **Complexity** | Simple cloning logic | Complex creation logic |
| **Use Case** | When copying is cheaper than creating | When creation logic is complex |

### Example Comparison:

**Factory Pattern:**
```python
# Creates new objects from scratch
zombie = ZombieFactory.create_zombie()  # Expensive initialization
```

**Prototype Pattern:**
```python
# Clones existing prototype
zombie = zombie_prototype.clone()  # Fast copying
```

## Real-World Examples

### 1. Game Development
```python
# NPCs in games - expensive to initialize with AI, graphics, etc.
zombie_prototype = Zombie()  # Expensive initialization once
zombie1 = zombie_prototype.clone()  # Fast cloning
zombie2 = zombie_prototype.clone()  # Fast cloning
```

### 2. Document Templates
```python
# Word processing applications
resume_template = ResumeTemplate()  # Complex formatting setup
resume1 = resume_template.clone()  # Quick copy
resume2 = resume_template.clone()  # Quick copy
```

### 3. Database Records
```python
# Database record templates
user_template = UserRecord()  # Expensive database setup
user1 = user_template.clone()  # Fast record creation
user2 = user_template.clone()  # Fast record creation
```

### 4. Configuration Objects
```python
# Application configuration
config_prototype = AppConfig()  # Complex configuration loading
dev_config = config_prototype.clone()  # Quick environment copy
prod_config = config_prototype.clone()  # Quick environment copy
```

### 5. Graphic Objects
```python
# CAD or graphic design applications
circle_prototype = Circle()  # Complex rendering setup
circle1 = circle_prototype.clone()  # Fast shape copying
circle2 = circle_prototype.clone()  # Fast shape copying
```

## Key Components

### 1. Prototype Interface
```python
from abc import ABC, abstractmethod

class Prototype(ABC):
    @abstractmethod
    def clone(self) -> 'Prototype':
        """Create a copy of this object"""
        pass
```

### 2. Concrete Prototype
```python
import copy

class ConcretePrototype(Prototype):
    def __init__(self, data):
        self.data = data
        self.complex_state = self._expensive_initialization()
    
    def _expensive_initialization(self):
        # Simulate expensive initialization
        return "Complex initialized state"
    
    def clone(self) -> 'ConcretePrototype':
        # Deep copy to avoid shared references
        return copy.deepcopy(self)
```

### 3. Prototype Manager (Optional)
```python
class PrototypeManager:
    def __init__(self):
        self.prototypes = {}
    
    def register_prototype(self, key: str, prototype: Prototype):
        self.prototypes[key] = prototype
    
    def create_object(self, key: str) -> Prototype:
        if key not in self.prototypes:
            raise ValueError(f"Unknown prototype: {key}")
        return self.prototypes[key].clone()
```

## Advantages and Drawbacks

### Advantages

#### 1. **Performance Optimization**
- Avoids expensive object creation
- Cloning is typically faster than full initialization
- Reduces memory allocation overhead

#### 2. **Runtime Flexibility**
- Add new object types at runtime
- Remove object types dynamically
- Modify prototypes without changing client code

#### 3. **Memory Efficiency**
- Shared prototype data
- Reduced memory footprint
- Efficient for similar objects

#### 4. **Independence from Classes**
- Client code doesn't depend on concrete classes
- Easy to add new prototype types
- Flexible object creation

#### 5. **Configuration Management**
- Easy to create variations of objects
- Prototype can be configured once
- Multiple instances share configuration

### Drawbacks

#### 1. **Cloning Complexity**
- Deep vs shallow copy considerations
- Circular reference handling
- Complex object state copying

#### 2. **Memory Management**
- Shared references can cause issues
- Need to handle prototype lifecycle
- Potential memory leaks if not managed properly

#### 3. **Limited Customization**
- Hard to customize individual instances
- All clones start with same state
- May need additional configuration after cloning

#### 4. **Debugging Difficulty**
- Harder to trace object creation
- Shared state can cause unexpected behavior
- Complex object relationships

## When to Use

### ✅ Use Prototype Pattern When:

1. **Expensive Object Creation**
   - Object initialization is costly
   - Database connections, file I/O, network calls
   - Complex calculations or processing

2. **Similar Objects Needed**
   - Many objects with similar structure
   - Small variations between instances
   - Template-based object creation

3. **Runtime Object Types**
   - Need to add/remove object types at runtime
   - Dynamic object creation requirements
   - Plugin-based architectures

4. **Memory Constraints**
   - Limited memory available
   - Need to share common data
   - Efficient object creation required

5. **Configuration Objects**
   - Complex configuration setup
   - Multiple environments (dev, test, prod)
   - Template-based configurations

### Example Scenarios:
- Game development (NPCs, items, levels)
- Document processing (templates, forms)
- Database applications (record templates)
- Graphics applications (shapes, sprites)
- Configuration management (app settings)

## When NOT to Use

### ❌ Avoid Prototype Pattern When:

1. **Simple Object Creation**
   - Object creation is already fast
   - No expensive initialization
   - Simple constructor calls

2. **Unique Objects**
   - Each object is significantly different
   - No benefit from copying
   - Custom initialization needed

3. **Immutable Objects**
   - Objects don't change after creation
   - No need for shared state
   - Value objects

4. **Complex Cloning**
   - Objects have complex relationships
   - Circular references
   - Deep copying is problematic

### Example Anti-Patterns:
```python
# Don't use Prototype for simple objects
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# This is overkill
point = point_prototype.clone()
# This is better
point = Point(10, 20)
```

## Costly Object Creation

The Prototype pattern is particularly valuable when object creation is expensive:

### 1. **Database Connections**
```python
class DatabaseConnection:
    def __init__(self):
        # Expensive: network connection, authentication, setup
        self.connection = self._establish_connection()
        self.schema = self._load_schema()
        self.permissions = self._load_permissions()
    
    def clone(self):
        # Fast: just copy the established connection
        return copy.deepcopy(self)
```

### 2. **File Processing**
```python
class DocumentProcessor:
    def __init__(self, file_path):
        # Expensive: file I/O, parsing, validation
        self.content = self._load_file(file_path)
        self.metadata = self._extract_metadata()
        self.structure = self._analyze_structure()
    
    def clone(self):
        # Fast: copy processed data
        return copy.deepcopy(self)
```

### 3. **Network Resources**
```python
class APIClient:
    def __init__(self, base_url):
        # Expensive: authentication, token generation, setup
        self.base_url = base_url
        self.auth_token = self._authenticate()
        self.endpoints = self._discover_endpoints()
    
    def clone(self):
        # Fast: reuse authenticated client
        return copy.deepcopy(self)
```

### 4. **Complex Calculations**
```python
class MathProcessor:
    def __init__(self, data):
        # Expensive: complex mathematical operations
        self.data = data
        self.statistics = self._calculate_statistics()
        self.models = self._train_models()
    
    def clone(self):
        # Fast: copy calculated results
        return copy.deepcopy(self)
```

## Runtime Object Management

The Prototype pattern enables dynamic object management:

### 1. **Adding Prototypes at Runtime**
```python
class PrototypeRegistry:
    def __init__(self):
        self.prototypes = {}
    
    def add_prototype(self, key: str, prototype: Prototype):
        """Add new prototype type at runtime"""
        self.prototypes[key] = prototype
        print(f"Added prototype: {key}")
    
    def create_object(self, key: str) -> Prototype:
        if key not in self.prototypes:
            raise ValueError(f"Unknown prototype: {key}")
        return self.prototypes[key].clone()
```

### 2. **Removing Prototypes at Runtime**
```python
def remove_prototype(self, key: str):
    """Remove prototype type at runtime"""
    if key in self.prototypes:
        del self.prototypes[key]
        print(f"Removed prototype: {key}")
    else:
        print(f"Prototype {key} not found")
```

### 3. **Dynamic Configuration**
```python
def configure_prototype(self, key: str, **kwargs):
    """Configure prototype at runtime"""
    if key in self.prototypes:
        prototype = self.prototypes[key]
        for attr, value in kwargs.items():
            setattr(prototype, attr, value)
        print(f"Configured prototype: {key}")
```

### 4. **Plugin Architecture**
```python
def load_plugin(self, plugin_path: str):
    """Load new prototype from plugin"""
    plugin = importlib.import_module(plugin_path)
    prototype = plugin.create_prototype()
    self.add_prototype(plugin.name, prototype)
```

## Composition over Inheritance

The Prototype pattern supports composition over inheritance:

### 1. **Composition-Based Prototypes**
```python
class Weapon:
    def __init__(self, damage, range):
        self.damage = damage
        self.range = range

class Armor:
    def __init__(self, defense, durability):
        self.defense = defense
        self.durability = durability

class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.weapon = None  # Composition
        self.armor = None   # Composition
    
    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
    
    def equip_armor(self, armor: Armor):
        self.armor = armor
    
    def clone(self):
        cloned = copy.deepcopy(self)
        return cloned
```

### 2. **Flexible Object Assembly**
```python
# Create character with different equipment combinations
warrior_prototype = Character("Warrior", 100)
warrior_prototype.equip_weapon(Weapon(50, 2))
warrior_prototype.equip_armor(Armor(30, 100))

archer_prototype = Character("Archer", 80)
archer_prototype.equip_weapon(Weapon(30, 5))
archer_prototype.equip_armor(Armor(20, 80))

# Clone with different configurations
warrior1 = warrior_prototype.clone()
archer1 = archer_prototype.clone()
```

### 3. **Behavioral Composition**
```python
class Behavior:
    def execute(self, character):
        pass

class AttackBehavior(Behavior):
    def execute(self, character):
        print(f"{character.name} attacks!")

class DefendBehavior(Behavior):
    def execute(self, character):
        print(f"{character.name} defends!")

class Character:
    def __init__(self, name):
        self.name = name
        self.behaviors = []  # Composition
    
    def add_behavior(self, behavior: Behavior):
        self.behaviors.append(behavior)
    
    def clone(self):
        return copy.deepcopy(self)
```

## Implementation Example

See `npc_prototype.py` for a complete implementation example of the Prototype pattern in a game NPC system.

### Key Features of the Example:
- **Abstract Prototype**: `NPC` class with `clone()` method
- **Concrete Prototypes**: `Zombie`, `Goblin`, `Orc` classes
- **Prototype Manager**: `NPCPrototypeManager` for managing prototypes
- **Runtime Modifications**: Add/remove prototypes at runtime
- **Game Simulation**: Battle scenario demonstrating pattern usage

### Running the Example:
```bash
python3 npc_prototype.py
```

## Best Practices

### 1. **Deep vs Shallow Copying**
```python
import copy

class Prototype:
    def clone(self):
        # Use deep copy for complex objects
        return copy.deepcopy(self)
    
    def shallow_clone(self):
        # Use shallow copy for simple objects
        return copy.copy(self)
```

### 2. **Prototype Registry**
```python
class PrototypeRegistry:
    def __init__(self):
        self.prototypes = {}
    
    def register(self, key: str, prototype: Prototype):
        self.prototypes[key] = prototype
    
    def create(self, key: str) -> Prototype:
        if key not in self.prototypes:
            raise ValueError(f"Unknown prototype: {key}")
        return self.prototypes[key].clone()
```

### 3. **Error Handling**
```python
def clone(self) -> 'Prototype':
    try:
        return copy.deepcopy(self)
    except Exception as e:
        raise CloneError(f"Failed to clone {self.__class__.__name__}: {e}")
```

### 4. **Memory Management**
```python
class PrototypeManager:
    def __init__(self):
        self.prototypes = {}
        self.weak_refs = weakref.WeakValueDictionary()
    
    def register_prototype(self, key: str, prototype: Prototype):
        self.prototypes[key] = prototype
        self.weak_refs[key] = prototype
```

### 5. **Validation**
```python
def clone(self) -> 'Prototype':
    cloned = copy.deepcopy(self)
    if not cloned.validate():
        raise ValidationError("Cloned object is invalid")
    return cloned
```

## Common Variations

### 1. **Registry-Based Prototype**
```python
class PrototypeRegistry:
    _prototypes = {}
    
    @classmethod
    def register(cls, key: str, prototype: Prototype):
        cls._prototypes[key] = prototype
    
    @classmethod
    def create(cls, key: str) -> Prototype:
        return cls._prototypes[key].clone()
```

### 2. **Factory-Prototype Hybrid**
```python
class PrototypeFactory:
    def __init__(self):
        self.prototypes = {}
    
    def create_object(self, type_name: str, **kwargs) -> Prototype:
        if type_name in self.prototypes:
            # Use prototype
            return self.prototypes[type_name].clone()
        else:
            # Fall back to factory creation
            return self._create_from_scratch(type_name, **kwargs)
```

### 3. **Lazy Prototype**
```python
class LazyPrototype:
    def __init__(self, factory_func):
        self._factory_func = factory_func
        self._prototype = None
    
    def clone(self) -> 'Prototype':
        if self._prototype is None:
            self._prototype = self._factory_func()
        return copy.deepcopy(self._prototype)
```

### 4. **Configurable Prototype**
```python
class ConfigurablePrototype:
    def __init__(self, base_config):
        self.config = base_config
    
    def clone_with_config(self, **overrides) -> 'ConfigurablePrototype':
        cloned = copy.deepcopy(self)
        cloned.config.update(overrides)
        return cloned
```

## Conclusion

The Prototype pattern is a powerful tool for optimizing object creation when initialization is expensive or when you need to create many similar objects. It provides runtime flexibility, memory efficiency, and independence from concrete classes.

Key takeaways:
- Use when object creation is expensive
- Enables runtime object type management
- Supports composition over inheritance
- Provides memory efficiency through shared prototypes
- Allows flexible object creation without class dependencies
- Consider cloning complexity and memory management
- Implement proper error handling and validation
