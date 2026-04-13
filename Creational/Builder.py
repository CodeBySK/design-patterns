# =============================================================================
# BUILDER PATTERN
# Separates the construction of a complex object from its representation,
# allowing the same process to produce different representations.
# =============================================================================


# =============================================================================
# WITHOUT Builder — Problem
# All configuration is pushed into one telescoping constructor. With many
# optional fields, callers must remember argument order and pass None/defaults
# for every field they don't care about.
# =============================================================================

class Pizza_NoPattern:
    def __init__(self, size, crust, sauce, cheese, toppings, extra_cheese,
                 gluten_free, vegan_cheese, thin_crust, stuffed_crust):
        self.size         = size
        self.crust        = crust
        self.sauce        = sauce
        self.cheese       = cheese
        self.toppings     = toppings
        self.extra_cheese = extra_cheese
        self.gluten_free  = gluten_free
        self.vegan_cheese = vegan_cheese
        self.thin_crust   = thin_crust
        self.stuffed_crust = stuffed_crust

    def __str__(self):
        return (f"Pizza(size={self.size}, crust={self.crust}, sauce={self.sauce}, "
                f"cheese={self.cheese}, toppings={self.toppings}, "
                f"extra_cheese={self.extra_cheese}, gluten_free={self.gluten_free})")


def without_builder():
    print("--- WITHOUT Builder ---")
    # Caller must provide ALL arguments even though most are irrelevant.
    # Extremely easy to mix up positional arguments.
    pizza = Pizza_NoPattern(
        size="large",
        crust="thin",
        sauce="tomato",
        cheese="mozzarella",
        toppings=["mushrooms", "peppers"],
        extra_cheese=False,
        gluten_free=False,
        vegan_cheese=False,
        thin_crust=True,
        stuffed_crust=False,
    )
    print(pizza)


# =============================================================================
# WITH Builder — Solution
# Construction is broken into readable, chainable steps. The director
# encodes standard recipes; the builder handles the actual assembly.
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Pizza:
    size: str          = "medium"
    crust: str         = "regular"
    sauce: str         = "tomato"
    cheese: str        = "mozzarella"
    toppings: List[str] = field(default_factory=list)
    extra_cheese: bool  = False
    gluten_free: bool   = False

    def __str__(self):
        return (f"Pizza(size={self.size}, crust={self.crust}, sauce={self.sauce}, "
                f"cheese={self.cheese}, toppings={self.toppings}, "
                f"extra_cheese={self.extra_cheese}, gluten_free={self.gluten_free})")


class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def size(self, size: str) -> PizzaBuilder:
        self._pizza.size = size
        return self

    def crust(self, crust: str) -> PizzaBuilder:
        self._pizza.crust = crust
        return self

    def sauce(self, sauce: str) -> PizzaBuilder:
        self._pizza.sauce = sauce
        return self

    def cheese(self, cheese: str) -> PizzaBuilder:
        self._pizza.cheese = cheese
        return self

    def add_topping(self, topping: str) -> PizzaBuilder:
        self._pizza.toppings.append(topping)
        return self

    def extra_cheese(self) -> PizzaBuilder:
        self._pizza.extra_cheese = True
        return self

    def gluten_free(self) -> PizzaBuilder:
        self._pizza.gluten_free = True
        return self

    def build(self) -> Pizza:
        return self._pizza


# Director encodes named recipes so callers don't repeat configuration steps.
class PizzaDirector:
    @staticmethod
    def margherita(builder: PizzaBuilder) -> Pizza:
        return (builder
                .size("medium")
                .crust("thin")
                .sauce("tomato")
                .cheese("mozzarella")
                .build())

    @staticmethod
    def veggie_supreme(builder: PizzaBuilder) -> Pizza:
        return (builder
                .size("large")
                .crust("regular")
                .sauce("pesto")
                .cheese("gouda")
                .add_topping("mushrooms")
                .add_topping("peppers")
                .add_topping("olives")
                .gluten_free()
                .build())


def with_builder():
    print("\n--- WITH Builder ---")

    # Using director for a known recipe
    margherita = PizzaDirector.margherita(PizzaBuilder())
    print(f"Margherita: {margherita}")

    # Custom order — only set what you actually care about
    custom = (PizzaBuilder()
              .size("small")
              .sauce("bbq")
              .add_topping("chicken")
              .add_topping("onions")
              .extra_cheese()
              .build())
    print(f"Custom:     {custom}")

    # Director recipe
    veggie = PizzaDirector.veggie_supreme(PizzaBuilder())
    print(f"Veggie:     {veggie}")


if __name__ == "__main__":
    without_builder()
    with_builder()
