"""
Prototype Pattern Example - Game NPC System

The Prototype pattern allows you to copy existing objects without making your code
dependent on their classes. It's particularly useful when object creation is expensive
and you need multiple similar instances.
"""

import copy
from abc import ABC, abstractmethod
from typing import Dict, Any


class NPC(ABC):
    """Abstract prototype class for Non-Player Characters"""
    
    def __init__(self, name: str, health: int, attack_power: int, speed: int):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.speed = speed
        self.position = (0, 0)
        self.is_alive = True
    
    @abstractmethod
    def clone(self) -> 'NPC':
        """Create a copy of this NPC"""
        pass
    
    def attack(self, target: 'NPC') -> None:
        """Attack another NPC"""
        if self.is_alive and target.is_alive:
            damage = self.attack_power
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} for {damage} damage!")
    
    def take_damage(self, damage: int) -> None:
        """Take damage and check if NPC dies"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} takes {damage} damage. Health: {self.health}")
    
    def move(self, x: int, y: int) -> None:
        """Move NPC to new position"""
        self.position = (x, y)
        print(f"{self.name} moves to position ({x}, {y})")
    
    def __str__(self) -> str:
        status = "Alive" if self.is_alive else "Dead"
        return f"{self.__class__.__name__}: {self.name} - Health: {self.health}, Attack: {self.attack_power}, Speed: {self.speed}, Status: {status}"


class Zombie(NPC):
    """Concrete prototype for Zombie NPCs"""
    
    def __init__(self, name: str = "Zombie", health: int = 80, attack_power: int = 15, speed: int = 5):
        super().__init__(name, health, attack_power, speed)
        self.undead = True
        self.regeneration = 2
    
    def clone(self) -> 'Zombie':
        """Create a deep copy of this Zombie"""
        cloned_zombie = copy.deepcopy(self)
        # Give the clone a unique name
        cloned_zombie.name = f"{self.name}_Clone_{id(cloned_zombie)}"
        return cloned_zombie
    
    def regenerate(self) -> None:
        """Zombies slowly regenerate health"""
        if self.is_alive:
            self.health += self.regeneration
            print(f"{self.name} regenerates {self.regeneration} health. New health: {self.health}")


class Goblin(NPC):
    """Concrete prototype for Goblin NPCs"""
    
    def __init__(self, name: str = "Goblin", health: int = 50, attack_power: int = 12, speed: int = 8):
        super().__init__(name, health, attack_power, speed)
        self.stealth = True
        self.critical_chance = 0.2
    
    def clone(self) -> 'Goblin':
        """Create a deep copy of this Goblin"""
        cloned_goblin = copy.deepcopy(self)
        # Give the clone a unique name
        cloned_goblin.name = f"{self.name}_Clone_{id(cloned_goblin)}"
        return cloned_goblin
    
    def sneak_attack(self, target: 'NPC') -> None:
        """Goblins can perform sneak attacks with higher damage"""
        if self.is_alive and target.is_alive:
            damage = int(self.attack_power * 1.5)
            target.take_damage(damage)
            print(f"{self.name} performs a sneak attack on {target.name} for {damage} damage!")


class Orc(NPC):
    """Concrete prototype for Orc NPCs"""
    
    def __init__(self, name: str = "Orc", health: int = 120, attack_power: int = 25, speed: int = 3):
        super().__init__(name, health, attack_power, speed)
        self.berserker_rage = False
        self.rage_damage_bonus = 10
    
    def clone(self) -> 'Orc':
        """Create a deep copy of this Orc"""
        cloned_orc = copy.deepcopy(self)
        # Give the clone a unique name
        cloned_orc.name = f"{self.name}_Clone_{id(cloned_orc)}"
        return cloned_orc
    
    def enter_berserker_rage(self) -> None:
        """Orcs can enter berserker rage for increased damage"""
        self.berserker_rage = True
        self.attack_power += self.rage_damage_bonus
        print(f"{self.name} enters berserker rage! Attack power increased to {self.attack_power}")


class NPCPrototypeManager:
    """Manages NPC prototypes and handles cloning"""
    
    def __init__(self):
        self.prototypes: Dict[str, NPC] = {}
        self._initialize_prototypes()
    
    def _initialize_prototypes(self) -> None:
        """Initialize all NPC prototypes"""
        print("Initializing NPC prototypes...")
        
        # Create prototype instances (expensive operation done once)
        self.prototypes["zombie"] = Zombie("Zombie_Prototype")
        self.prototypes["goblin"] = Goblin("Goblin_Prototype")
        self.prototypes["orc"] = Orc("Orc_Prototype")
        
        print("NPC prototypes initialized successfully!\n")
    
    def create_npc(self, npc_type: str) -> NPC:
        """Create a new NPC by cloning the prototype"""
        if npc_type not in self.prototypes:
            raise ValueError(f"Unknown NPC type: {npc_type}")
        
        prototype = self.prototypes[npc_type]
        cloned_npc = prototype.clone()
        print(f"Created new {npc_type} from prototype: {cloned_npc.name}")
        return cloned_npc
    
    def add_prototype(self, npc_type: str, prototype: NPC) -> None:
        """Add a new prototype at runtime"""
        self.prototypes[npc_type] = prototype
        print(f"Added new prototype: {npc_type}")
    
    def remove_prototype(self, npc_type: str) -> None:
        """Remove a prototype at runtime"""
        if npc_type in self.prototypes:
            del self.prototypes[npc_type]
            print(f"Removed prototype: {npc_type}")
    
    def list_prototypes(self) -> None:
        """List all available prototypes"""
        print("Available NPC prototypes:")
        for npc_type, prototype in self.prototypes.items():
            print(f"  - {npc_type}: {prototype}")


def simulate_game_scenario():
    """Simulate a game scenario using the Prototype pattern"""
    
    print("=== Game Scenario: NPC Battle ===\n")
    
    # Initialize the prototype manager
    npc_manager = NPCPrototypeManager()
    
    # Create multiple NPCs using prototypes (fast cloning)
    print("Creating NPCs for battle...")
    zombies = [npc_manager.create_npc("zombie") for _ in range(3)]
    goblins = [npc_manager.create_npc("goblin") for _ in range(2)]
    orcs = [npc_manager.create_npc("orc") for _ in range(1)]
    
    print(f"\nCreated {len(zombies)} zombies, {len(goblins)} goblins, {len(orcs)} orcs\n")
    
    # Position NPCs
    print("Positioning NPCs...")
    for i, zombie in enumerate(zombies):
        zombie.move(i * 10, 0)
    
    for i, goblin in enumerate(goblins):
        goblin.move(i * 15, 5)
    
    for orc in orcs:
        orc.move(25, 10)
    
    print()
    
    # Simulate battle
    print("=== Battle Begins! ===")
    
    # Zombies attack goblins
    for zombie in zombies:
        if zombie.is_alive and goblins:
            target = goblins[0]
            zombie.attack(target)
            if target.is_alive:
                zombie.regenerate()
    
    print()
    
    # Goblins use special abilities
    for goblin in goblins:
        if goblin.is_alive and zombies:
            target = zombies[0]
            goblin.sneak_attack(target)
    
    print()
    
    # Orc enters berserker rage
    for orc in orcs:
        if orc.is_alive:
            orc.enter_berserker_rage()
            if zombies:
                orc.attack(zombies[0])
    
    print()
    
    # Show final status
    print("=== Battle Results ===")
    all_npcs = zombies + goblins + orcs
    for npc in all_npcs:
        print(npc)
    
    print(f"\nSurvivors: {sum(1 for npc in all_npcs if npc.is_alive)}/{len(all_npcs)}")


def demonstrate_runtime_modifications():
    """Demonstrate adding/removing prototypes at runtime"""
    
    print("\n=== Runtime Prototype Modifications ===\n")
    
    npc_manager = NPCPrototypeManager()
    
    # List current prototypes
    npc_manager.list_prototypes()
    
    # Add a new prototype at runtime
    print("\nAdding new prototype...")
    dragon = Orc("Dragon", 200, 50, 2)  # Create a dragon-like orc
    dragon.name = "Dragon_Prototype"
    npc_manager.add_prototype("dragon", dragon)
    
    # Create NPC from new prototype
    new_dragon = npc_manager.create_npc("dragon")
    print(f"Created dragon: {new_dragon}")
    
    # Remove a prototype
    print("\nRemoving goblin prototype...")
    npc_manager.remove_prototype("goblin")
    
    # Try to create removed prototype (should fail)
    try:
        npc_manager.create_npc("goblin")
    except ValueError as e:
        print(f"Error: {e}")
    
    # List updated prototypes
    print("\nUpdated prototypes:")
    npc_manager.list_prototypes()


def main():
    """Main function demonstrating the Prototype pattern"""
    
    print("=== Prototype Pattern Demo - Game NPC System ===\n")
    
    # Demonstrate basic prototype usage
    simulate_game_scenario()
    
    # Demonstrate runtime modifications
    demonstrate_runtime_modifications()
    
    print("\n=== Prototype Pattern Benefits ===")
    print("✓ Avoid expensive object creation by cloning prototypes")
    print("✓ Add/remove object types at runtime")
    print("✓ Reduce memory usage through shared prototypes")
    print("✓ Flexible object creation without knowing concrete classes")
    print("✓ Easy to create variations of existing objects")


if __name__ == "__main__":
    main()
