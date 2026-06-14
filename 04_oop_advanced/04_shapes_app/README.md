# 04 — Shapes App: every advanced-OOP idea in one place

A small, runnable `.py` app that uses **every concept from this folder together**.

## Files

- [`shapes.py`](shapes.py) — `Shape` ABC + `Circle`, `Rectangle`, `Triangle` as `@dataclass(frozen=True)`. Each implements `area`/`perimeter` (abstract methods). `Circle` also uses `@property` for `diameter`.
- [`canvas.py`](canvas.py) — a `Canvas` class that **has-a** list of shapes (composition, *not* inheritance). It iterates over them polymorphically.
- [`demo.py`](demo.py) — assembles the pieces.
- [`test_shapes.py`](test_shapes.py) — `assert`-based tests. Will move to `pytest` in folder 09.

## Run it

```powershell
python 04_oop_advanced\04_shapes_app\demo.py
python 04_oop_advanced\04_shapes_app\test_shapes.py
```

## What this demonstrates

| Concept | Where in the code |
|---|---|
| ABC + `@abstractmethod` | `Shape` in `shapes.py` |
| Inheritance + `super()` | `Shape.__post_init__` validation called by subclasses' generated `__init__` |
| `@dataclass(frozen=True)` | every concrete shape — immutable value objects |
| `@property` | `Circle.diameter`, `Canvas.total_area` |
| Polymorphism (no isinstance) | `Canvas.summary()` iterates and calls `area`/`perimeter` |
| Composition (has-a, not is-a) | `Canvas` holds a `list[Shape]`; it does NOT inherit from anything |

## Why "Square inherits Rectangle" is **not** here

The classic anti-example. A mathematical square *is-a* rectangle, but if `Square` inherits
from `Rectangle` and `Rectangle.width` is settable, you can break the square's invariant
(`width == height`). This is the **Liskov Substitution Principle** violation — a subclass
that isn't safely substitutable for its base.

If you want a square, build it as another `Shape` subclass (or compose a `Rectangle`).
Don't inherit. We model `Triangle` directly in `shapes.py` for the same reason — no fake
"is-a" relationships.

## Try this

1. Add `RegularPolygon(sides: int, side_length: float)` to `shapes.py` with the right
   `area`/`perimeter` formulas. Confirm `Canvas.summary()` picks it up with **no changes
   to Canvas** — that's polymorphism doing its job.
2. Add a `Canvas.scale(factor)` method that returns a *new* Canvas with every shape scaled.
   Since shapes are `frozen=True`, you have to construct new instances. Why is that a
   feature, not a bug?
3. Make `Canvas` itself a `@dataclass` (`shapes: list[Shape] = field(default_factory=list)`).
   What did the rewrite save? What did it cost (read: `__init__` validation)?
