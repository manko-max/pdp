# State Pattern

## Table of Contents
1. [Overview](#overview)
2. [Definition](#definition)
3. [Real-World Examples](#real-world-examples)
4. [Key Elements](#key-elements)
5. [Advantages and Drawbacks](#advantages-and-drawbacks)
6. [When to Use](#when-to-use)
7. [When NOT to Use](#when-not-to-use)
8. [Behavioral Changes](#behavioral-changes)
9. [Eliminating Conditionals](#eliminating-conditionals)
10. [Single Responsibility](#single-responsibility)
11. [State Transitions](#state-transitions)
12. [Implementation Example](#implementation-example)
13. [Best Practices](#best-practices)
14. [Common Variations](#common-variations)

## Overview

The State pattern is a behavioral design pattern that allows an object to alter its behavior when its internal state changes. The object will appear to change its class, but it's actually delegating behavior to different state objects.

## Definition

**State Pattern**: A design pattern that allows an object to change its behavior when its internal state changes. The object will appear to change its class, but it's actually delegating behavior to different state objects.

### Key Characteristics:
- **State-dependent behavior**: Object behavior changes based on current state
- **State encapsulation**: Each state is encapsulated in its own class
- **State transitions**: Clear transitions between different states
- **No conditionals**: Eliminates long if-else or switch statements

## Real-World Examples

### 1. Media Player
```python
# Different behaviors based on state
player.play()   # Behavior depends on current state
player.pause()  # Playing -> Pause, Stopped -> Error
player.stop()   # Any state -> Stopped
```

### 2. Traffic Light System
```python
# Traffic light states
traffic_light.change()  # Red -> Green -> Yellow -> Red
traffic_light.stop()    # Different behavior in each state
```

### 3. Vending Machine
```python
# Vending machine states
machine.insert_coin()   # NoCoin -> HasCoin
machine.select_item()   # HasCoin -> Sold
machine.dispense()      # Sold -> NoCoin
```

### 4. Game Character
```python
# Character states
character.move()        # Idle -> Walking, Walking -> Running
character.attack()      # Different attacks based on state
character.defend()      # Different defense based on state
```

### 5. Document Workflow
```python
# Document states
document.submit()       # Draft -> Pending
document.approve()      # Pending -> Approved
document.reject()       # Pending -> Rejected
```

## Key Elements

### 1. State Interface
```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def action1(self, context):
        pass
    
    @abstractmethod
    def action2(self, context):
        pass
```

### 2. Concrete States
```python
class ConcreteStateA(State):
    def action1(self, context):
        print("State A handling action1")
        context.set_state(ConcreteStateB())
    
    def action2(self, context):
        print("State A handling action2")
```

### 3. Context Class
```python
class Context:
    def __init__(self):
        self.current_state = ConcreteStateA()
    
    def set_state(self, new_state):
        self.current_state = new_state
    
    def action1(self):
        self.current_state.action1(self)
    
    def action2(self):
        self.current_state.action2(self)
```

## Advantages and Drawbacks

### Advantages

#### 1. **Eliminates Conditionals**
- No long if-else statements
- No complex switch cases
- Cleaner, more maintainable code

#### 2. **Single Responsibility**
- Each state class has one responsibility
- Easy to understand and modify
- Clear separation of concerns

#### 3. **Easy to Add New States**
- Just create new state class
- No need to modify existing code
- Open/closed principle compliance

#### 4. **State Transitions**
- Clear state transition logic
- Easy to track state changes
- Predictable behavior

#### 5. **Testability**
- Each state can be tested independently
- Easy to mock states for testing
- Clear test boundaries

### Drawbacks

#### 1. **Complexity**
- More classes and interfaces
- Can be overkill for simple state machines
- Steeper learning curve

#### 2. **State Explosion**
- Many states can lead to many classes
- Hard to manage with complex state machines
- Potential for state transition bugs

#### 3. **Memory Usage**
- Each state is a separate object
- More memory overhead
- State objects need to be managed

#### 4. **Debugging**
- Harder to trace state transitions
- State changes can be implicit
- Complex state relationships

## When to Use

### ✅ Use State Pattern When:

1. **State-Dependent Behavior**
   - Object behavior changes based on state
   - Multiple states with different behaviors
   - Clear state transitions

2. **Complex Conditionals**
   - Long if-else statements
   - Complex switch cases
   - State-dependent logic

3. **State Machine**
   - Clear states and transitions
   - Predictable state changes
   - State validation needed

4. **Behavioral Changes**
   - Object needs to change behavior
   - Runtime state changes
   - Dynamic behavior switching

5. **Maintainability**
   - Need to add new states frequently
   - Want to avoid modifying existing code
   - Clear separation of concerns

### Example Scenarios:
- Media players (play, pause, stop)
- Traffic lights (red, yellow, green)
- Vending machines (no coin, has coin, sold)
- Game characters (idle, walking, running, attacking)
- Document workflows (draft, pending, approved, rejected)

## When NOT to Use

### ❌ Avoid State Pattern When:

1. **Simple State Logic**
   - Only a few states
   - Simple state transitions
   - No complex behavior changes

2. **Performance Critical**
   - State changes happen frequently
   - Memory usage is a concern
   - Need maximum performance

3. **Stateless Objects**
   - Object doesn't have states
   - Behavior is always the same
   - No state-dependent logic

4. **Complex State Relationships**
   - Many interconnected states
   - Complex state dependencies
   - Hard to model with classes

### Example Anti-Patterns:
```python
# Don't use State for simple cases
class SimpleCounter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1  # Simple, no states needed
```

## Behavioral Changes

The State pattern allows objects to change behavior dynamically:

### 1. **State-Dependent Actions**
```python
class MediaPlayer:
    def play(self):
        # Behavior depends on current state
        self.current_state.play(self)
    
    def pause(self):
        # Different behavior in each state
        self.current_state.pause(self)
```

### 2. **Dynamic Behavior Switching**
```python
class PlayingState(State):
    def play(self, player):
        print("Already playing!")  # Different behavior
    
    def pause(self, player):
        print("Pausing...")        # Different behavior
        player.set_state(PausedState())
```

### 3. **Context-Aware Actions**
```python
class StoppedState(State):
    def play(self, player):
        print("Starting playback...")  # Context-aware behavior
        player.set_state(PlayingState())
    
    def pause(self, player):
        print("Cannot pause - not playing!")  # Context-aware behavior
```

## Eliminating Conditionals

The State pattern eliminates complex conditional logic:

### 1. **Before State Pattern (Bad)**
```python
class MediaPlayer:
    def __init__(self):
        self.state = "stopped"
    
    def play(self):
        if self.state == "stopped":
            print("Starting playback...")
            self.state = "playing"
        elif self.state == "paused":
            print("Resuming...")
            self.state = "playing"
        elif self.state == "playing":
            print("Already playing!")
        else:
            print("Invalid state!")
    
    def pause(self):
        if self.state == "playing":
            print("Pausing...")
            self.state = "paused"
        elif self.state == "paused":
            print("Already paused!")
        elif self.state == "stopped":
            print("Cannot pause - not playing!")
        else:
            print("Invalid state!")
```

### 2. **After State Pattern (Good)**
```python
class MediaPlayer:
    def __init__(self):
        self.current_state = StoppedState()
    
    def play(self):
        self.current_state.play(self)  # No conditionals!
    
    def pause(self):
        self.current_state.pause(self)  # No conditionals!
```

## Single Responsibility

The State pattern supports the Single Responsibility Principle:

### 1. **Each State Has One Responsibility**
```python
class PlayingState(State):
    # Responsibility: Handle behavior when playing
    def play(self, player):
        print("Already playing!")
    
    def pause(self, player):
        print("Pausing...")
        player.set_state(PausedState())
    
    def stop(self, player):
        print("Stopping...")
        player.set_state(StoppedState())
```

### 2. **Context Class Responsibility**
```python
class MediaPlayer:
    # Responsibility: Manage state and delegate actions
    def __init__(self):
        self.current_state = StoppedState()
    
    def set_state(self, new_state):
        self.current_state = new_state
    
    def play(self):
        self.current_state.play(self)
```

### 3. **Clear Separation of Concerns**
- **State classes**: Handle state-specific behavior
- **Context class**: Manage state transitions
- **No mixing**: Each class has one clear purpose

## State Transitions

The State pattern provides clear state transitions:

### 1. **Defined State Transitions**
```python
class PlayingState(State):
    def pause(self, player):
        player.set_state(PausedState())  # Clear transition
    
    def stop(self, player):
        player.set_state(StoppedState())  # Clear transition
```

### 2. **State Transition Diagram**
```
StoppedState --play--> PlayingState
PlayingState --pause--> PausedState
PlayingState --stop--> StoppedState
PausedState --play--> PlayingState
PausedState --stop--> StoppedState
```

### 3. **Invalid Transitions**
```python
class StoppedState(State):
    def pause(self, player):
        print("Cannot pause - not playing!")  # Invalid transition
```

## Implementation Example

See `media_player.py` for a complete implementation example of the State pattern in a digital media player.

### Key Features of the Example:
- **State Interface**: `State` abstract class with play, pause, stop methods
- **Concrete States**: `PlayingState`, `PausedState`, `StoppedState`
- **Context Class**: `MediaPlayer` that delegates to current state
- **State Transitions**: Clear transitions between states
- **No Conditionals**: Clean, maintainable code

### Running the Example:
```bash
python3 media_player.py
```

## Best Practices

### 1. **State Interface Design**
```python
class State(ABC):
    @abstractmethod
    def action1(self, context):
        pass
    
    @abstractmethod
    def action2(self, context):
        pass
```

### 2. **State Transitions**
```python
class ConcreteState(State):
    def action(self, context):
        # Perform action
        print("Performing action...")
        
        # Transition to new state
        context.set_state(NewState())
```

### 3. **State Validation**
```python
class Context:
    def set_state(self, new_state):
        if self.is_valid_transition(self.current_state, new_state):
            self.current_state = new_state
        else:
            raise InvalidStateTransitionError()
```

### 4. **State History**
```python
class Context:
    def __init__(self):
        self.current_state = InitialState()
        self.state_history = [InitialState()]
    
    def set_state(self, new_state):
        self.current_state = new_state
        self.state_history.append(new_state)
```

### 5. **State Factory**
```python
class StateFactory:
    @staticmethod
    def create_state(state_type):
        if state_type == "playing":
            return PlayingState()
        elif state_type == "paused":
            return PausedState()
        elif state_type == "stopped":
            return StoppedState()
        else:
            raise ValueError(f"Unknown state: {state_type}")
```

## Common Variations

### 1. **State with Entry/Exit Actions**
```python
class State(ABC):
    def enter(self, context):
        pass
    
    def exit(self, context):
        pass
    
    @abstractmethod
    def action(self, context):
        pass

class PlayingState(State):
    def enter(self, context):
        print("Entering playing state...")
    
    def exit(self, context):
        print("Exiting playing state...")
    
    def action(self, context):
        print("Playing...")
```

### 2. **Hierarchical States**
```python
class BaseState(State):
    def action(self, context):
        print("Base state action")

class PlayingState(BaseState):
    def action(self, context):
        super().action(context)  # Call parent
        print("Playing state specific action")
```

### 3. **State with Data**
```python
class State(ABC):
    def __init__(self, data=None):
        self.data = data or {}
    
    def action(self, context):
        # Use state data
        print(f"Action with data: {self.data}")
```

### 4. **State Machine**
```python
class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.transitions = {}
    
    def add_state(self, name, state):
        self.states[name] = state
    
    def add_transition(self, from_state, to_state, action):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][action] = to_state
    
    def transition(self, action):
        if self.current_state in self.transitions:
            if action in self.transitions[self.current_state]:
                new_state = self.transitions[self.current_state][action]
                self.current_state = new_state
                return True
        return False
```

## Conclusion

The State pattern is a powerful tool for managing state-dependent behavior in objects. It eliminates complex conditionals, provides clear state transitions, and supports the Single Responsibility Principle.

Key takeaways:
- Use when object behavior changes based on state
- Eliminates long if-else statements
- Each state has single responsibility
- Easy to add new states
- Clear state transitions
- Consider complexity vs. benefits
- Implement proper state validation
- Use for state machines and workflows
