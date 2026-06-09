---
name: curriculum
description: The ordered roadmap of topics for this Python → FastAPI → Agentic AI learning project, plus a progress tracker. Use whenever the user asks "what's next", says "next learning", asks how far we are, or asks to reorder/skip topics. This file is the single source of truth for sequencing.
---

# Curriculum — Fastest effective path to FastAPI + Agentic AI

Designed so each topic unlocks the next. Earlier folders are kept small; later folders are
where the real production-shaped code lives. Estimated time assumes 1–2 focused sessions per topic.

## Progress tracker

Legend: `[ ]` not started · `[~]` in progress · `[x]` done.

- [x] **00_foundations** — syntax, variables, types, control flow, functions, modules, imports, `if __name__ == "__main__"`, running `.py` vs `.ipynb`.
- [x] **01_data_structures** — list, tuple, dict, set; slicing; comprehensions; iteration; `enumerate`/`zip`; mutability; copy vs reference.
- [~] **02_functions_deep** — args/kwargs, default values, `*args`/`**kwargs`, closures, first-class functions, lambdas, decorators (intro), `functools.wraps`.
- [ ] **03_oop_basics** — classes, instances, `__init__`, `self`, instance vs class attributes, methods, `@classmethod`, `@staticmethod`, `__repr__`/`__str__`.
- [ ] **04_oop_advanced** — inheritance, `super()`, polymorphism, abstract base classes (`abc.ABC`), `@dataclass`, `@property`, composition over inheritance.
- [ ] **05_typing_and_protocols** — `list[int]`, `dict[str, T]`, `Optional`, `Union` / `|`, generics (`TypeVar`, `Generic`), `Protocol` (structural typing) vs `ABC`, `typing.Annotated`.
- [ ] **06_errors_and_context** — exception hierarchy, custom exceptions, `try/except/else/finally`, `raise from`, context managers (`with`, `contextlib.contextmanager`, `__enter__`/`__exit__`).
- [ ] **07_iterators_generators** — `iter`/`next`, generator functions, `yield`, `yield from`, generator expressions, lazy pipelines.
- [ ] **08_modules_and_packages** — package layout, relative vs absolute imports, `__init__.py`, editable installs, `src/` layout, virtualenvs (recap), running as `python -m`.
- [ ] **09_testing_with_pytest** — `pytest` basics, fixtures, parametrize, `tmp_path`, mocking with `unittest.mock`, structuring `tests/`.
- [ ] **10_pydantic_v2** — `BaseModel`, field types, validation, `field_validator`/`model_validator`, `Settings` via `pydantic-settings`, serialization.
- [ ] **11_async_basics** — event loop, `async def` / `await`, `asyncio.gather`, `asyncio.run`, async iteration, when async helps and when it doesn't.
- [ ] **12_di_and_services** — what DI actually is, constructor injection by hand, service layer pattern, repository pattern, why frameworks add DI containers, light DI container example.
- [ ] **13_fastapi_basics** — app + routes, path/query/body params, Pydantic request/response models, `Depends`, error responses, OpenAPI docs.
- [ ] **14_fastapi_advanced** — dependency injection with `Depends` chains, middleware, background tasks, lifespan events, settings via pydantic-settings, structured logging, testing FastAPI with `TestClient`.
- [ ] **15_llm_client_basics** — calling the Anthropic API (chat, system prompt, streaming), token thinking, structured output via Pydantic, error handling, retries.
- [ ] **16_agent_loops** — what an "agent" is (model + tools + loop), tool definitions, parallel tool calls, the agent loop pattern, exit conditions.
- [ ] **17_agentic_service** — wrapping an agent loop behind a FastAPI service: routes, dependency-injected agent, streaming responses, observability basics.

## Reordering / skipping rules

- The user may ask to skip a topic. If they do, mark it `[skip]` with a one-line reason in the bullet, and proceed to the next.
- If the user requests a topic out of order, do it — but warn them about any unmet prereq once, then proceed.
- New folders may be inserted (e.g. an `11a_async_patterns` for extra practice). Use letter suffixes so numbering stays stable.

## How this file is used

The [learning skill](../learning/SKILL.md) reads this file to decide what to scaffold next.
On "next learning":

1. Flip the current `[~]` topic to `[x]`.
2. Flip the next `[ ]` topic to `[~]`.
3. Create that folder per the learning skill's rules.

Do not edit this list silently — if topics are added/removed/reordered, mention it in chat so the user stays oriented.
