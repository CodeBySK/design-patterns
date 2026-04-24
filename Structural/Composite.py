# =============================================================================
# COMPOSITE PATTERN
# Composes objects into tree structures to represent part-whole hierarchies.
# Clients treat individual objects and compositions uniformly.
# =============================================================================


# =============================================================================
# WITHOUT Composite — Problem
# The code that calculates total price must know whether it is dealing with
# a single item or a bundle. Every new container type forces the caller to
# add a new branch — the client is coupled to the concrete structure.
# =============================================================================

class Item_NoPattern:
    def __init__(self, name: str, price: float):
        self.name  = name
        self.price = price

class Bundle_NoPattern:
    def __init__(self, name: str):
        self.name  = name
        self.items: list[Item_NoPattern] = []

    def add(self, item: Item_NoPattern):
        self.items.append(item)


def get_total_no_pattern(thing) -> float:
    # Caller must type-check — breaks every time a new container type appears.
    if isinstance(thing, Item_NoPattern):
        return thing.price
    elif isinstance(thing, Bundle_NoPattern):
        return sum(item.price for item in thing.items)
    raise TypeError(f"Unknown type: {type(thing)}")


def without_composite():
    print("--- WITHOUT Composite ---")
    book  = Item_NoPattern("Python Book", 29.99)
    mouse = Item_NoPattern("Mouse",       19.99)

    bundle = Bundle_NoPattern("Starter Kit")
    bundle.add(book)
    bundle.add(mouse)

    print(f"Book total:   ${get_total_no_pattern(book):.2f}")
    print(f"Bundle total: ${get_total_no_pattern(bundle):.2f}")


# =============================================================================
# WITH Composite — Solution
# Both leaf (Item) and composite (Bundle) implement the same Component
# interface. Callers call `total_price()` on anything without knowing
# whether it is a leaf or a subtree.
# =============================================================================

from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def total_price(self) -> float: pass

    @abstractmethod
    def display(self, indent: int = 0): pass


class Item(Component):
    def __init__(self, name: str, price: float):
        self.name  = name
        self.price = price

    def total_price(self) -> float:
        return self.price

    def display(self, indent: int = 0):
        print(" " * indent + f"- {self.name}: ${self.price:.2f}")


class Bundle(Component):
    def __init__(self, name: str):
        self.name       = name
        self._children: list[Component] = []

    def add(self, component: Component):
        self._children.append(component)

    def total_price(self) -> float:
        return sum(child.total_price() for child in self._children)

    def display(self, indent: int = 0):
        print(" " * indent + f"[{self.name}]  total=${self.total_price():.2f}")
        for child in self._children:
            child.display(indent + 2)


def with_composite():
    print("\n--- WITH Composite ---")
    book      = Item("Python Book", 29.99)
    mouse     = Item("Mouse",       19.99)
    keyboard  = Item("Keyboard",    49.99)

    peripherals = Bundle("Peripherals")
    peripherals.add(mouse)
    peripherals.add(keyboard)

    office_bundle = Bundle("Office Bundle")
    office_bundle.add(book)
    office_bundle.add(peripherals)   # nested bundle

    # Same call regardless of depth or structure
    office_bundle.display()
    print(f"\nGrand total: ${office_bundle.total_price():.2f}")


if __name__ == "__main__":
    without_composite()
    with_composite()
