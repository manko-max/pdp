"""
Builder Pattern Example - Restaurant Meal Ordering System

The Builder pattern allows you to construct complex objects step by step.
It's particularly useful when you have objects with many optional parameters
or when you want to create different representations of the same product.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Meal:
    """The product class - represents a complete meal"""
    
    def __init__(self):
        self.main_course: Optional[str] = None
        self.side: Optional[str] = None
        self.drink: Optional[str] = None
    
    def __str__(self):
        return f"Meal: {self.main_course} + {self.side} + {self.drink}"


class MealBuilder(ABC):
    """Abstract builder interface"""
    
    def __init__(self):
        self.meal = Meal()
    
    @abstractmethod
    def set_main_course(self) -> 'MealBuilder':
        pass
    
    @abstractmethod
    def set_side(self) -> 'MealBuilder':
        pass
    
    @abstractmethod
    def set_drink(self) -> 'MealBuilder':
        pass
    
    def build(self) -> Meal:
        return self.meal


class BurgerMealBuilder(MealBuilder):
    """Concrete builder for burger meals"""
    
    def set_main_course(self) -> 'MealBuilder':
        self.meal.main_course = "Cheeseburger"
        return self
    
    def set_side(self) -> 'MealBuilder':
        self.meal.side = "French Fries"
        return self
    
    def set_drink(self) -> 'MealBuilder':
        self.meal.drink = "Cola"
        return self


class PizzaMealBuilder(MealBuilder):
    """Concrete builder for pizza meals"""
    
    def set_main_course(self) -> 'MealBuilder':
        self.meal.main_course = "Margherita Pizza"
        return self
    
    def set_side(self) -> 'MealBuilder':
        self.meal.side = "Garlic Bread"
        return self
    
    def set_drink(self) -> 'MealBuilder':
        self.meal.drink = "Orange Juice"
        return self


class SaladMealBuilder(MealBuilder):
    """Concrete builder for healthy salad meals"""
    
    def set_main_course(self) -> 'MealBuilder':
        self.meal.main_course = "Caesar Salad"
        return self
    
    def set_side(self) -> 'MealBuilder':
        self.meal.side = "Soup"
        return self
    
    def set_drink(self) -> 'MealBuilder':
        self.meal.drink = "Green Tea"
        return self


class MealDirector:
    """Director class that orchestrates the building process"""
    
    def __init__(self, builder: MealBuilder):
        self.builder = builder
    
    def construct_meal(self) -> Meal:
        """Constructs a meal using the provided builder"""
        return (self.builder
                .set_main_course()
                .set_side()
                .set_drink()
                .build())


def main():
    """Demonstrates the Builder pattern in action"""
    
    print("=== Restaurant Meal Ordering System ===\n")
    
    # Create different types of meals using the Builder pattern
    
    # 1. Burger Meal
    print("1. Creating Burger Meal:")
    burger_builder = BurgerMealBuilder()
    burger_director = MealDirector(burger_builder)
    burger_meal = burger_director.construct_meal()
    print(f"   {burger_meal}\n")
    
    # 2. Pizza Meal
    print("2. Creating Pizza Meal:")
    pizza_builder = PizzaMealBuilder()
    pizza_director = MealDirector(pizza_builder)
    pizza_meal = pizza_director.construct_meal()
    print(f"   {pizza_meal}\n")
    
    # 3. Salad Meal
    print("3. Creating Salad Meal:")
    salad_builder = SaladMealBuilder()
    salad_director = MealDirector(salad_builder)
    salad_meal = salad_director.construct_meal()
    print(f"   {salad_meal}\n")
    
    # 4. Direct builder usage (without director)
    print("4. Direct Builder Usage:")
    custom_builder = BurgerMealBuilder()
    custom_meal = (custom_builder
                   .set_main_course()
                   .set_side()
                   .set_drink()
                   .build())
    print(f"   {custom_meal}\n")
    
    print("=== Builder Pattern Benefits ===")
    print("✓ Step-by-step object construction")
    print("✓ Different representations using same construction process")
    print("✓ Fluent interface for readable code")
    print("✓ Easy to add new meal types")
    print("✓ Separation of construction logic from representation")


if __name__ == "__main__":
    main()
