"""A small Shape hierarchy showing every advanced-OOP idea together.

  - `Shape` is an `abc.ABC` defining the contract (area, perimeter).
  - Concrete shapes are `@dataclass(frozen=True)` — immutable, hashable value objects.
  - Validation runs in `__post_init__` so it works with dataclass-generated `__init__`.
  - `Circle.diameter` is a `@property` (computed attribute, no parens at the call site).
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Shape(ABC):
    """Abstract base for any 2D shape.

    Concrete subclasses must implement `area` and `perimeter`. The non-abstract
    `describe` method lives here so every Shape gets it for free — this is the
    "template method" pattern.
    """

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        # type(self).__name__ gives the concrete class's name — Circle, Rectangle, etc.
        return (
            f"{type(self).__name__}("
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f})"
        )


@dataclass(frozen=True)
class Circle(Shape):
    radius: float

    # __post_init__ is dataclass's hook for validation. It runs AFTER the generated
    # __init__ has set the fields. For frozen dataclasses you cannot reassign here —
    # only validate.
    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError(f"radius must be positive: {self.radius}")

    @property
    def diameter(self) -> float:
        return self.radius * 2

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


@dataclass(frozen=True)
class Rectangle(Shape):
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                f"width and height must be positive: {self.width}, {self.height}"
            )

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


@dataclass(frozen=True)
class Triangle(Shape):
    """Isoceles triangle defined by base + height.

    We model Triangle as its own Shape rather than inheriting from Rectangle/Square —
    inheritance should only be for genuine is-a relationships.
    """

    base: float
    height: float

    def __post_init__(self) -> None:
        if self.base <= 0 or self.height <= 0:
            raise ValueError(
                f"base and height must be positive: {self.base}, {self.height}"
            )

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        # isoceles: two equal slants meeting at the apex
        slant = math.hypot(self.base / 2, self.height)
        return self.base + 2 * slant


if __name__ == "__main__":
    # Smoke test when run directly.
    shapes: list[Shape] = [Circle(3), Rectangle(2, 4), Triangle(6, 4)]
    for s in shapes:
        print(s.describe())
    print("Circle(3).diameter =", Circle(3).diameter)
