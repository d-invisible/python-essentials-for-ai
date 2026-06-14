"""Demo of the shapes app — assembles ABC, dataclass, property, composition, polymorphism.

Run:
    python 04_oop_advanced\\04_shapes_app\\demo.py
"""

from canvas import Canvas
from shapes import Circle, Rectangle, Shape, Triangle


def main() -> None:
    # ---- 1. Frozen dataclasses give us value-object semantics for free ----
    a = Circle(3)
    b = Circle(3)
    print("Circle(3) == Circle(3) ?", a == b)            # True
    print("Hashable?", {a, b})                            # collapses to one
    print("Circle(3).diameter (via @property):", a.diameter)
    print()

    # ---- 2. ABC enforces the contract ----
    try:
        Shape()                                           # type: ignore[abstract]
    except TypeError as e:
        print("Cannot instantiate the ABC directly:", e)
    print()

    # ---- 3. Validation runs in __post_init__ ----
    print("trying invalid constructions:")
    for label, action in [
        ("Circle(-1)", lambda: Circle(-1)),
        ("Rectangle(0, 5)", lambda: Rectangle(0, 5)),
        ("Triangle(3, -2)", lambda: Triangle(3, -2)),
    ]:
        try:
            action()
            print(f"  {label}: (no error — bug!)")
        except ValueError as e:
            print(f"  {label}: rejected -> {e}")
    print()

    # ---- 4. Polymorphism via the Canvas (composition) ----
    canvas = Canvas("my-art")
    canvas.add(Circle(3))
    canvas.add(Rectangle(2, 4))
    canvas.add(Triangle(6, 4))
    print(canvas.summary())
    print()

    # ---- 5. Canvas exposes shapes as an IMMUTABLE tuple — callers can't reach in ----
    print("canvas.shapes type:", type(canvas.shapes).__name__)
    try:
        canvas.shapes[0] = Circle(99)                     # type: ignore[index]
    except TypeError as e:
        print("encapsulation holds:", e)


if __name__ == "__main__":
    main()
