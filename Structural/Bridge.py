# =============================================================================
# BRIDGE PATTERN
# Decouples an abstraction from its implementation so that the two can vary
# independently. Avoids a class explosion when combining multiple dimensions.
# =============================================================================


# =============================================================================
# WITHOUT Bridge — Problem
# Each combination of shape × renderer requires its own class.
# Two shapes × two renderers = four classes; adding a third renderer means
# adding two more classes, and so on — an exponential explosion.
# =============================================================================

class CircleRasterRenderer_NoPattern:
    def draw(self, radius: float):
        print(f"[Raster] Drawing circle  (radius={radius})")

class CircleVectorRenderer_NoPattern:
    def draw(self, radius: float):
        print(f"[Vector] Drawing circle  (radius={radius})")

class SquareRasterRenderer_NoPattern:
    def draw(self, side: float):
        print(f"[Raster] Drawing square  (side={side})")

class SquareVectorRenderer_NoPattern:
    def draw(self, side: float):
        print(f"[Vector] Drawing square  (side={side})")


def without_bridge():
    print("--- WITHOUT Bridge ---")
    CircleRasterRenderer_NoPattern().draw(5)
    CircleVectorRenderer_NoPattern().draw(5)
    SquareRasterRenderer_NoPattern().draw(4)
    SquareVectorRenderer_NoPattern().draw(4)


# =============================================================================
# WITH Bridge — Solution
# The Renderer hierarchy (implementation) is separated from the Shape hierarchy
# (abstraction). Each dimension grows independently — adding a new renderer
# requires only one new class, not one per shape.
# =============================================================================

from abc import ABC, abstractmethod


# ---------- Implementation hierarchy ----------

class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius: float): pass

    @abstractmethod
    def render_square(self, side: float): pass


class RasterRenderer(Renderer):
    def render_circle(self, radius: float):
        print(f"[Raster] Drawing circle  (radius={radius})")

    def render_square(self, side: float):
        print(f"[Raster] Drawing square  (side={side})")


class VectorRenderer(Renderer):
    def render_circle(self, radius: float):
        print(f"[Vector] Drawing circle  (radius={radius})")

    def render_square(self, side: float):
        print(f"[Vector] Drawing square  (side={side})")


# ---------- Abstraction hierarchy ----------

class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer   # bridge to the implementation

    @abstractmethod
    def draw(self): pass


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float):
        super().__init__(renderer)
        self._radius = radius

    def draw(self):
        self._renderer.render_circle(self._radius)


class Square(Shape):
    def __init__(self, renderer: Renderer, side: float):
        super().__init__(renderer)
        self._side = side

    def draw(self):
        self._renderer.render_square(self._side)


def with_bridge():
    print("\n--- WITH Bridge ---")
    renderers = [RasterRenderer(), VectorRenderer()]
    for renderer in renderers:
        Circle(renderer, 5).draw()
        Square(renderer, 4).draw()


if __name__ == "__main__":
    without_bridge()
    with_bridge()
