# =============================================================================
# DECORATOR PATTERN
# Attaches additional responsibilities to an object dynamically.
# Provides a flexible alternative to subclassing for extending functionality.
# =============================================================================


# =============================================================================
# WITHOUT Decorator — Problem
# Every feature combination requires its own subclass. With N features you
# need up to 2^N subclasses, and adding a new feature forces changes to
# every existing combination class.
# =============================================================================

class PlainCoffee_NoPattern:
    def cost(self) -> float:
        return 1.00

    def description(self) -> str:
        return "Plain coffee"

class MilkCoffee_NoPattern(PlainCoffee_NoPattern):
    def cost(self) -> float:
        return super().cost() + 0.25

    def description(self) -> str:
        return super().description() + ", milk"

class SugarMilkCoffee_NoPattern(MilkCoffee_NoPattern):
    def cost(self) -> float:
        return super().cost() + 0.10

    def description(self) -> str:
        return super().description() + ", sugar"

# Adding "vanilla" requires yet another class (VanillaMilkCoffee,
# VanillaSugarMilkCoffee, VanillaPlainCoffee …) — the list explodes.


def without_decorator():
    print("--- WITHOUT Decorator ---")
    coffee = SugarMilkCoffee_NoPattern()
    print(f"{coffee.description()}  →  ${coffee.cost():.2f}")


# =============================================================================
# WITH Decorator — Solution
# Decorators wrap a component and add behaviour without subclassing.
# Any combination is assembled at runtime by stacking wrappers.
# =============================================================================

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: pass

    @abstractmethod
    def description(self) -> str: pass


class PlainCoffee(Coffee):
    def cost(self) -> float:
        return 1.00

    def description(self) -> str:
        return "Plain coffee"


class CoffeeDecorator(Coffee):
    """Base decorator — forwards calls to the wrapped component."""
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.25

    def description(self) -> str:
        return super().description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.10

    def description(self) -> str:
        return super().description() + ", sugar"


class VanillaDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.50

    def description(self) -> str:
        return super().description() + ", vanilla"


def with_decorator():
    print("\n--- WITH Decorator ---")

    # Plain
    coffee: Coffee = PlainCoffee()
    print(f"{coffee.description()}  →  ${coffee.cost():.2f}")

    # Add milk
    coffee = MilkDecorator(coffee)
    print(f"{coffee.description()}  →  ${coffee.cost():.2f}")

    # Also add sugar
    coffee = SugarDecorator(coffee)
    print(f"{coffee.description()}  →  ${coffee.cost():.2f}")

    # Totally different combo: vanilla + milk, no sugar
    fancy: Coffee = VanillaDecorator(MilkDecorator(PlainCoffee()))
    print(f"{fancy.description()}  →  ${fancy.cost():.2f}")


if __name__ == "__main__":
    without_decorator()
    with_decorator()
