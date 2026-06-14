"""Assert-based tests for the shapes app.

We'll convert these to `pytest` in folder 09_testing_with_pytest.

Run:
    python 04_oop_advanced\\04_shapes_app\\test_shapes.py
"""

import math

from canvas import Canvas
from shapes import Circle, Rectangle, Shape, Triangle


def test_abc_cannot_be_instantiated() -> None:
    try:
        Shape()  # type: ignore[abstract]
    except TypeError:
        return
    raise AssertionError("Shape() should have raised TypeError")


def test_circle_basics() -> None:
    c = Circle(3)
    assert math.isclose(c.area(), math.pi * 9)
    assert math.isclose(c.perimeter(), 2 * math.pi * 3)
    assert c.diameter == 6                          # @property — no parens
    # value semantics from @dataclass(frozen=True)
    assert c == Circle(3)
    assert hash(c) == hash(Circle(3))


def test_frozen_is_immutable() -> None:
    c = Circle(3)
    try:
        c.radius = 99  # type: ignore[misc]
    except Exception:                              # FrozenInstanceError subclasses AttributeError
        return
    raise AssertionError("frozen dataclass field should be immutable")


def test_validation_in_post_init() -> None:
    for ctor in [
        lambda: Circle(-1),
        lambda: Circle(0),
        lambda: Rectangle(2, -3),
        lambda: Rectangle(0, 5),
        lambda: Triangle(-1, 4),
    ]:
        try:
            ctor()
        except ValueError:
            continue
        raise AssertionError("expected ValueError, got none")


def test_canvas_composition_and_polymorphism() -> None:
    c = Canvas("test")
    c.add(Circle(1))
    c.add(Rectangle(2, 3))
    c.add(Triangle(4, 2))

    # Polymorphic sum — no isinstance, no type-dispatch.
    expected = math.pi * 1 + 2 * 3 + 0.5 * 4 * 2
    assert math.isclose(c.total_area, expected), c.total_area

    # Summary mentions every concrete class name (proves polymorphism worked).
    s = c.summary()
    assert "Circle" in s and "Rectangle" in s and "Triangle" in s


def test_canvas_returns_immutable_view() -> None:
    c = Canvas("test")
    c.add(Circle(1))
    assert isinstance(c.shapes, tuple), "shapes should be a tuple, not a list"
    try:
        c.shapes[0] = Circle(99)  # type: ignore[index]
    except TypeError:
        return
    raise AssertionError("tuple should not be assignable")


def test_canvas_rejects_non_shape() -> None:
    c = Canvas("test")
    try:
        c.add("not a shape")  # type: ignore[arg-type]
    except TypeError:
        return
    raise AssertionError("expected TypeError when adding a non-Shape")


def main() -> None:
    tests = [
        test_abc_cannot_be_instantiated,
        test_circle_basics,
        test_frozen_is_immutable,
        test_validation_in_post_init,
        test_canvas_composition_and_polymorphism,
        test_canvas_returns_immutable_view,
        test_canvas_rejects_non_shape,
    ]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    main()
