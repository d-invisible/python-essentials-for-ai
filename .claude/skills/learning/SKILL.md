---
name: learning
description: Rules and workflow for the Python → FastAPI → Agentic AI learning project. Use whenever the user asks for a learning step, scaffolds a new topic folder, runs notebooks/scripts, or says "next learning". Governs file layout, dependency handling, and teaching style for this project.
---

# Learning Skill — How we work through this curriculum

This project teaches Python from basics through OOP, services/DI, FastAPI, and agentic AI.
Use this skill on every learning-related turn in this project.

## Core rules

1. **One topic folder at a time.** Do not scaffold the next folder until the user says **"next learning"** (or an obvious equivalent like "next topic", "move on"). When they do, read [curriculum](../curriculum/SKILL.md), find the next unchecked topic, create that folder, and mark progress.

2. **Folder naming.** `NN_snake_case_topic` where `NN` is two-digit zero-padded (e.g. `00_foundations`, `07_async_basics`). Match the number in the curriculum.

3. **File format choice — pick deliberately per sub-topic, not per folder:**
   - **`.ipynb` (Jupyter)** for: exploratory concepts, REPL-style learning, things where seeing intermediate values matters (data structures, comprehensions, pandas-style work, prompt experiments).
   - **`.py`** for: anything that models real-world structure — modules, packages, classes, services, DI containers, FastAPI apps, tests, agent loops. Production-shaped code goes in `.py`.
   - A single folder can mix both. Prefer `.py` once we're past pure-syntax topics.

4. **Every topic folder contains:**
   - `README.md` — objectives (3–6 bullets), prerequisites, file map, "you'll be able to…" outcomes, and 3–5 **exercises** at the end.
   - One or more `.ipynb` / `.py` files covering the concepts in teaching order.
   - For `.py`-heavy topics: a `tests/` subfolder or `test_*.py` files using `pytest`, so the user learns testing alongside the topic.

5. **Dependencies — venv + requirements.txt only.**
   - Never `pip install` globally. Always activate `.venv` or use `uv pip install` against it.
   - When a topic needs a new library, **append it to `requirements.txt`** (uncomment if already listed) with a minimum version, then install via `uv pip install -r requirements.txt`. Tell the user which lines you added.
   - Never use `pyproject.toml` for deps in this project — the user explicitly chose `requirements.txt`.

6. **Run before declaring done.**
   - For `.py` files: execute them (or their tests) and show output.
   - For `.ipynb` files: at minimum, validate they parse; ideally execute cells via `jupyter nbconvert --to notebook --execute` or `jupyter execute` and report success.
   - If something can't be executed in this environment, say so explicitly.

7. **Teaching-code comments are allowed.** This is a *learning* repo — the global "no comments" rule does not apply here. Use comments to explain *why* a concept matters, *what* a syntax form means the first time it appears, and to point out gotchas. Don't over-comment trivia.

8. **Build up, don't dump.** Each notebook/script should introduce ≤ 1 major new idea per cell/section, with a runnable example, then a small twist, then an exercise prompt. Avoid 200-line monoliths.

9. **Cross-link.** When a topic builds on a previous folder, link it: `See [03_oop_advanced/README.md](../03_oop_advanced/README.md)`. When a topic foreshadows a future one, mention it: "We'll use this when we get to FastAPI dependencies."

10. **Update curriculum progress.** When a folder is scaffolded, mark its checkbox `[~]` (in progress) in [curriculum/SKILL.md](../curriculum/SKILL.md). When the user confirms they're done with a topic (or says "next learning"), flip it to `[x]` before creating the next folder.

## Workflow on "next learning"

1. Read [curriculum/SKILL.md](../curriculum/SKILL.md).
2. Find the first topic whose checkbox is `[ ]` or `[~]`. If the current one is `[~]`, mark it `[x]`.
3. Mark the next one `[~]`.
4. Create its folder with `README.md` + initial file(s).
5. Add any new dependencies to `requirements.txt`, install, confirm.
6. Tell the user what was created and where to start (which file, which section).

## Workflow on a topic-specific question

- If the question is about a concept inside the **current** topic folder, answer in chat and/or extend the existing files in that folder.
- Do **not** create a new folder just because a tangential question came up — answer inline or add a small `notes.md` to the current folder.

## What to NOT do

- Do not pre-create all curriculum folders.
- Do not install packages into the system Python.
- Do not switch the project to `pyproject.toml`-managed deps without the user asking.
- Do not skip ahead in the curriculum without the user's go-ahead.
- Do not write essay-length explanations in the chat when the same material belongs in the topic's README/notebook.
