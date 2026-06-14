"""A `Canvas` that holds shapes.

This is the **composition** example — `Canvas` has-a list of `Shape`s. It does NOT
inherit from `Shape`, list, or anything else. That's deliberate: a canvas isn't a shape,
and inheriting from `list` would expose pointless methods (`.sort()`, `.pop()`) on it.

It also demonstrates **polymorphism** in `summary()` and `total_area` — the loop has no
clue what concrete types the shapes are, and doesn't care.
"""

from __future__ import annotations

from shapes import Shape


class Canvas:
    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("canvas name must be a non-empty string")
        self.name = name.strip()
        # Composition: a Canvas owns its list of shapes; the list isn't part of the
        # Canvas's identity, just its content.
        self._shapes: list[Shape] = []

    # ---- composition API ----
    def add(self, shape: Shape) -> None:
        if not isinstance(shape, Shape):
            raise TypeError(f"expected a Shape, got {type(shape).__name__}")
        self._shapes.append(shape)

    @property
    def shapes(self) -> tuple[Shape, ...]:
        # Return a tuple so callers can't mutate our internal list — encapsulation.
        return tuple(self._shapes)

    # ---- polymorphic behavior ----
    @property
    def total_area(self) -> float:
        # No isinstance, no type-dispatch. Every Shape promises an .area() method.
        return sum(s.area() for s in self._shapes)

    def summary(self) -> str:
        if not self._shapes:
            return f"Canvas {self.name!r} is empty."
        lines = [f"Canvas {self.name!r} contains {len(self._shapes)} shape(s):"]
        for s in self._shapes:
            lines.append(f"  - {s.describe()}")
        lines.append(f"Total area: {self.total_area:.2f}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Canvas(name={self.name!r}, shapes={len(self._shapes)})"


if __name__ == "__main__":
    from shapes import Circle, Rectangle, Triangle

    c = Canvas("smoke-test")
    c.add(Circle(3))
    c.add(Rectangle(2, 4))
    c.add(Triangle(6, 4))
    print(c.summary())
