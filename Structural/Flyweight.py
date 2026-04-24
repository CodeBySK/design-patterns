# =============================================================================
# FLYWEIGHT PATTERN
# Uses sharing to support a large number of fine-grained objects efficiently.
# Separates intrinsic (shared) state from extrinsic (per-instance) state.
# =============================================================================


# =============================================================================
# WITHOUT Flyweight — Problem
# Every tree stores its own full copy of species data (name, texture, color).
# With thousands of trees that share the same species, memory is wasted on
# duplicate data that is identical across instances.
# =============================================================================

import sys


class Tree_NoPattern:
    def __init__(self, x: int, y: int,
                 species: str, texture: str, color: str):
        self.x       = x
        self.y       = y
        self.species = species
        self.texture = texture   # large data duplicated per tree
        self.color   = color     # large data duplicated per tree


def without_flyweight():
    print("--- WITHOUT Flyweight ---")
    forest = [
        Tree_NoPattern(i, i * 2, "Oak", "rough_bark_texture_data", "#5C4033")
        for i in range(1000)
    ]
    sample = forest[0]
    print(f"Trees: {len(forest)}")
    print(f"Approx memory per tree: {sys.getsizeof(sample)} bytes")
    print(f"Approx total (rough):   {sys.getsizeof(sample) * len(forest):,} bytes")


# =============================================================================
# WITH Flyweight — Solution
# TreeType holds the shared (intrinsic) state and is cached by the factory.
# Tree only stores its unique (extrinsic) position — greatly reducing memory.
# =============================================================================

class TreeType:
    """Intrinsic state — shared across all trees of the same species."""
    def __init__(self, species: str, texture: str, color: str):
        self.species = species
        self.texture = texture
        self.color   = color

    def draw(self, x: int, y: int):
        print(f"Drawing {self.species} at ({x}, {y}) "
              f"color={self.color}")


class TreeTypeFactory:
    _cache: dict[str, TreeType] = {}

    @classmethod
    def get(cls, species: str, texture: str, color: str) -> TreeType:
        key = f"{species}_{color}"
        if key not in cls._cache:
            cls._cache[key] = TreeType(species, texture, color)
            print(f"[Factory] Created new TreeType: {species}")
        return cls._cache[key]


class Tree:
    """Extrinsic state — unique position per tree instance."""
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x         = x
        self.y         = y
        self.tree_type = tree_type   # shared reference, not a copy

    def draw(self):
        self.tree_type.draw(self.x, self.y)


def with_flyweight():
    print("\n--- WITH Flyweight ---")
    oak_type = TreeTypeFactory.get("Oak", "rough_bark_texture_data", "#5C4033")
    pine_type = TreeTypeFactory.get("Pine", "smooth_bark_texture_data", "#2D5A27")

    forest = [Tree(i, i * 2, oak_type) for i in range(500)]
    forest += [Tree(i, i * 3, pine_type) for i in range(500)]

    print(f"Trees: {len(forest)}")
    print(f"Unique TreeType objects: {len(TreeTypeFactory._cache)}")
    # Draw a sample
    for tree in forest[:3]:
        tree.draw()
    print("...")


if __name__ == "__main__":
    without_flyweight()
    with_flyweight()
