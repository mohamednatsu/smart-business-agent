# Daily Progress Log — Smart Business Agent

This file tracks the daily progress of the 20-Day Agentic AI Engineer Challenge.
Each entry follows the challenge's daily template.

## Progress Summary

| Day | Focus | Date | Tests | Status |
|-----|-------|------|-------|--------|
| 1 | Project foundation, typing, FastAPI, Pydantic | 2026-10-16 | 4 passed | ✅ Complete |
| 2 | LLM APIs and structured output | 2026-10-16 | 13 passed | ✅ Complete |
| 3 | Tool / function calling | — | — | 🔜 Next |

---

## Day 1 — Project Foundation, Python Typing, FastAPI, Pydantic

**Date:** 2026-10-16
**Day:** 1

### Topics Studied

- Project layout and virtual environments with `uv`
- Python type hints and Pydantic models
- FastAPI routes, request/response schemas, settings
- Pytest basics, HTTPX test client, Ruff linting and formatting

### References Completed

- uv getting started — https://docs.astral.sh/uv/getting-started/
- FastAPI tutorial — https://fastapi.tiangolo.com/tutorial/
- Pydantic documentation — https://docs.pydantic.dev/latest/
- pytest getting started — https://docs.pytest.org/en/stable/getting-started.html
- Ruff documentation — https://docs.astral.sh/ruff/

### Project Changes

- Initialized the `smart-business-agent` repository with `uv init`
- Pinned Python 3.12 in `.python-version`
- Added runtime dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`
- Added dev dependencies: `pytest`, `httpx`, `ruff`
- Created the project structure:
  - `app/main.py` — FastAPI app with `/health` endpoint
  - `app/config.py` — Pydantic `Settings` class with `SBA_` env prefix
  - `app/schemas/health.py` — `HealthResponse` model
  - `tests/test_health.py` — health endpoint tests
  - `tests/test_config.py` — settings defaults test
- Configured `pyproject.toml`:
  - `[tool.ruff]` with `E`, `W`, `F`, `I`, `UP`, `B`, `SIM` rules
  - `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `testpaths = ["tests"]`
- Added `.env.example` and `.gitignore`
- Wrote `README.md` with setup, run, test, and lint instructions

### Tests / Commands Run

```bash
uv sync
uv run pytest -v                   # 4 passed
uv run ruff check .                # clean
uv run fastapi dev app/main.py     # started on 127.0.0.1:8000
curl http://127.0.0.1:8000/health  # 200 OK
```

### What I Can Explain Without Notes

- Why settings use a `SBA_` prefix and are loaded from the environment instead of being hard-coded
- Why request and response bodies get their own Pydantic models rather than raw dicts
- Why linting and tests are set up on Day 1, before any business logic exists

### Issues and Next Actions

- No issues recorded.
- Next: Day 2 — LLM provider interface and structured output validation.

### Git Commit

`<paste commit hash / message here>`

---

## Day 2 — LLM APIs and Structured Output

**Date:** 2026-10-16
**Day:** 2

### Topics Studied

- Chat message structure: `system`, `user`, and `assistant` roles
- Structured output via JSON mode and Pydantic schema validation
- Provider abstraction and dependency injection in FastAPI
- Retry strategies with exponential backoff (`tenacity`)
- Mocking external APIs to keep tests deterministic and free

### References Completed

- Groq documentation — https://console.groq.com/docs/overview
- Groq structured outputs — https://console.groq.com/docs/structured-outputs
- OpenAI API concepts (compatible patterns) — https://platform.openai.com/docs/overview
- Pydantic models — https://docs.pydantic.dev/latest/concepts/models/
- Tenacity retry library — https://tenacity.readthedocs.io/

### Project Changes

- Added dependencies: `groq`, `tenacity`, `pytest-asyncio`, `pytest-mock`
- Extended `app/config.py` with LLM configuration:
  - `SBA_GROQ_API_KEY`
  - `SBA_LLM_MODEL` (default: `llama-3.3-70b-versatile`)
  - `SBA_LLM_TIMEOUT_SECONDS` (default: `30`)
  - `SBA_LLM_MAX_RETRIES` (default: `2`)
- Created new modules:
  - `app/schemas/task.py` — `BusinessTask`, `TaskType`, `LLMResponse`
  - `app/services/llm/interface.py` — `LLMProvider` ABC and `LLMProviderError`
  - `app/services/llm/groq_provider.py` — Groq implementation with system prompt, JSON parsing, and Pydantic validation
  - `app/services/llm/retry.py` — `tenacity`-based retry wrapper that skips schema errors
  - `app/services/llm/factory.py` — `get_llm_provider()` dependency provider
  - `app/api/tasks.py` — `POST /tasks` endpoint returning a validated `BusinessTask`
- Wired the router into `app/main.py`
- Added tests:
  - `tests/unit/test_task_schema.py` — schema validation edge cases
  - `tests/unit/test_groq_provider.py` — valid JSON, malformed JSON, schema violation, provider failure
  - `tests/integration/test_tasks_endpoint.py` — mocked provider through FastAPI
- Added `scripts/check_day.sh` and `scripts/check_day.ps1` — one-command day completion checks
- Updated `.env.example` with the Groq key placeholder
- Updated `README.md` to reflect the new architecture

### Tests / Commands Run

```bash
uv run pytest -v             # 13 passed
uv run ruff check --fix .    # clean
uv run ruff format .         # formatted
./scripts/check_day.sh       # ALL CHECKS PASSED
```

### What I Can Explain Without Notes

- Why the API layer depends on the `LLMProvider` interface instead of the Groq SDK, so a new provider is one new file plus a factory branch
- Why the LLM is treated as untrusted and every response is validated through `BusinessTask`
- Why `tenacity` retries only transient failures (timeouts, 5xx, rate limits) and not schema errors, which are deterministic
- Why a provider failure maps to HTTP 502 instead of a 500 stack trace
- Why the whole test suite is mocked: it stays fast, free, deterministic, and CI-friendly

### Issues and Next Actions

- No issues recorded.
- Next: Day 3 — read-only tools (`get_sales_summary`, `list_overdue_invoices`), argument validation, and a registry so only registered tools can run.

### Git Commit

`<paste commit hash / message here>`

---

## Daily Entry Template

Copy this block for each new day.

````markdown
## Day N — Title

**Date:**
**Day:**

### Topics Studied
-

### References Completed
-

### Project Changes
-

### Tests / Commands Run
```bash
```

### What I Can Explain Without Notes
-

### Issues and Next Actions
-

### Git Commit
`<hash / message>`
````