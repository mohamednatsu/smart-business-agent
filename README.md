# Smart Business Agent

> A portfolio-grade Agentic AI system for business operations, built incrementally over a 20-day engineering challenge.

[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063)](https://docs.pydantic.dev/)
[![Ruff](https://img.shields.io/badge/lint-ruff-000000)](https://docs.astral.sh/ruff/)
[![Tests](https://img.shields.io/badge/tests-pytest-0a9edc)](https://docs.pytest.org/)
[![Managed with uv](https://img.shields.io/badge/managed%20with-uv-de5fe9)](https://docs.astral.sh/uv/)

---

## Overview

**Smart Business Agent** is a business-operations assistant under active development. The end goal is a reliable, auditable agent that can:

- Answer questions about sales and overdue invoices from synthetic business data
- Retrieve company policies via retrieval-augmented generation (RAG)
- Execute **deterministic Python tools** for calculations and database access
- Cite sources and refuse to answer when evidence is insufficient
- Require **explicit human approval** before sensitive or irreversible actions
- Persist task history and audit records with tenant isolation

The project is built in small, testable increments. Every day adds one capability with tests, linting, and documentation updated in the same commit.

---

## Engineering Principles

The project follows the challenge's implementation rules strictly:

| Principle | Enforcement |
|---|---|
| **Deterministic business logic** | Calculations live in Python; the LLM only classifies intent |
| **Validated LLM output** | All model responses pass through Pydantic schemas |
| **Least-privilege tools** | The model can only request tools from an explicit registry |
| **Human-in-the-loop** | Sensitive actions require a recorded approval step |
| **Secrets hygiene** | Only `.env.example` is committed; `.env` is git-ignored |
| **Test-first provider mocking** | The full test suite runs with **no live LLM calls** |
| **Observability by default** | Trace IDs, structured logs, and redaction from Day 16 onward |

These are not aspirational — each one is enforced by code and tests by the day it appears in the plan.

---

## Current Status

| Day | Focus | Status |
|-----|-------|--------|
| 1 | Foundation: FastAPI, Pydantic, pytest, Ruff, uv | ✅ Complete |
| 2 | LLM provider interface, structured task output, retries | ✅ Complete |
| 3 | Tool / function calling | 🔜 Next |
| 4 | Agent execution loop with step limits | ⬜ Planned |
| 5 | State, context, conversation history | ⬜ Planned |
| 6 | Testing and evaluation foundations | ⬜ Planned |
| 7 | Consolidation — first milestone | ⬜ Planned |
| 8 | Embeddings and vector search | ⬜ Planned |
| 9 | Retrieval-augmented generation (RAG) | ⬜ Planned |
| 10 | Memory and persistence (PostgreSQL) | ⬜ Planned |
| 11 | LangGraph orchestration | ⬜ Planned |
| 12 | Human approval and resumable workflows | ⬜ Planned |
| 13 | Agent and RAG evaluation | ⬜ Planned |
| 14 | Production architecture and reliability | ⬜ Planned |
| 15 | Security and prompt injection | ⬜ Planned |
| 16 | Observability, latency, and cost | ⬜ Planned |
| 17 | Multi-agent patterns and trade-offs | ⬜ Planned |
| 18 | Model Context Protocol (MCP) | ⬜ Planned |
| 19 | Docker and deployment | ⬜ Planned |
| 20 | Final assessment and portfolio | ⬜ Planned |

The day-by-day engineering log — including references, decisions, and test evidence — lives in [`docs/daily-progress.md`](docs/daily-progress.md).

---

## Architecture (as of Day 2)

```
┌─────────────────────────────────────────────────────────────────┐
│                         HTTP Clients                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application (app/)                   │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │  /health     │  │  POST /tasks                             │ │
│  │              │  │  (validates input via Pydantic)          │ │
│  └──────────────┘  └────────────────────┬─────────────────────┘ │
│                                         │                       │
│                                         ▼                       │
│                          ┌──────────────────────────────┐       │
│                          │  LLMProvider (interface)     │       │
│                          │  ─ generate_task(str)        │       │
│                          └──────────────┬───────────────┘       │
│                                         │                       │
│                          ┌──────────────┴────────────┐          │
│                          │  GroqProvider             │          │
│                          │  + tenacity retry         │          │
│                          │  + Pydantic validation    │          │
│                          └──────────────┬────────────┘          │
└─────────────────────────────────────────┼───────────────────────┘
                                          │
                                          ▼
                          ┌──────────────────────────────┐
                          │  Groq Chat Completions API   │
                          │  (JSON mode)                 │
                          └──────────────────────────────┘
```

Key contracts:

- **`BusinessTask`** — the only shape the rest of the system accepts from an LLM
- **`LLMProvider`** — the only shape the API layer knows about
- **`LLMProviderError`** — the only failure type the API layer maps to HTTP 502

This separation means a new provider (OpenAI, local model, Anthropic) is a single new file plus a factory branch.

---

## Requirements

| Requirement | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Runtime |
| [uv](https://docs.astral.sh/uv/) | Latest | Environment and dependency management |
| Groq API key | Optional | Only required to call a real LLM; tests are mocked |

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/<your-user>/smart-business-agent.git
cd smart-business-agent

# 2. Sync environment
uv sync

# 3. (Optional) Configure a real LLM key
cp .env.example .env
# edit .env and set SBA_GROQ_API_KEY=gsk_...

# 4. Run the API
uv run fastapi dev app/main.py
```

The API is available at:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Liveness check for load balancers |
| `POST /tasks` | Classify a natural-language request into a validated task |
| `GET /docs` | Swagger UI |
| `GET /redoc` | ReDoc |

---

## API Reference

### `GET /health`

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

```json
{
  "status": "healthy",
  "service": "Smart Business Agent",
  "version": "0.1.0"
}
```

### `POST /tasks`

Converts a natural-language business request into a validated `BusinessTask`.

**Request**

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"request": "What were our sales last month?"}'
```

**Response (200)**

```json
{
  "task": {
    "task_type": "sales_summary",
    "tool_name": "get_sales_summary",
    "tool_arguments": { "period": "month" },
    "reasoning": "User asked about monthly sales."
  },
  "source": "llm"
}
```

**Error contract**

| Status | Condition |
|---|---|
| 422 | Request body failed Pydantic validation |
| 502 | `LLMProviderError` — provider failed, returned invalid JSON, or violated the schema |
| 500 | Unexpected application error |

---

## Development

### Run the test suite

```bash
uv run pytest -v
```

All provider calls are mocked — **no API key required**.

### Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

Auto-fix what is safe:

```bash
uv run ruff check --fix .
```

### Day completion check

Run this before every commit at the end of a day:

```bash
# macOS / Linux
./scripts/check_day.sh

# Windows PowerShell
.\scripts\check_day.ps1
```

The script runs:

1. `uv sync`
2. `ruff check --fix`
3. `ruff format`
4. `ruff format --check` (verification pass)
5. `pytest -v`
6. FastAPI import smoke test

It exits non-zero on any failure, so it doubles as a pre-commit gate.

---

## Configuration

All settings are environment-driven with the `SBA_` prefix.

| Variable | Default | Purpose |
|---|---|---|
| `SBA_APP_NAME` | `Smart Business Agent` | Display name |
| `SBA_APP_VERSION` | `0.1.0` | Semantic version |
| `SBA_DEBUG` | `false` | Debug mode |
| `SBA_LOG_LEVEL` | `INFO` | Logging level |
| `SBA_GROQ_API_KEY` | *(empty)* | Groq API key — required only for live LLM calls |
| `SBA_LLM_MODEL` | `llama-3.3-70b-versatile` | Groq model identifier |
| `SBA_LLM_TIMEOUT_SECONDS` | `30` | Timeout for a single LLM call |
| `SBA_LLM_MAX_RETRIES` | `2` | Retries for transient LLM failures |

Create `.env` from `.env.example` and set only what you need. `.env` is git-ignored.

---

## Project Layout

```
smart-business-agent/
├── app/
│   ├── api/
│   │   └── tasks.py                  # POST /tasks
│   ├── schemas/
│   │   ├── health.py                 # HealthResponse
│   │   └── task.py                   # BusinessTask, TaskType, LLMResponse
│   ├── services/
│   │   └── llm/
│   │       ├── interface.py          # LLMProvider ABC + LLMProviderError
│   │       ├── groq_provider.py      # Groq implementation
│   │       ├── retry.py              # tenacity retry wrapper
│   │       └── factory.py            # get_llm_provider()
│   ├── config.py                     # Pydantic Settings
│   └── main.py                       # FastAPI app
├── tests/
│   ├── unit/
│   │   ├── test_task_schema.py       # Schema validation
│   │   └── test_groq_provider.py     # Provider with mocked LLM
│   └── integration/
│       └── test_tasks_endpoint.py    # End-to-end through FastAPI
├── scripts/
│   ├── check_day.sh                  # Day completion check (bash)
│   └── check_day.ps1                 # Day completion check (PowerShell)
├── docs/
│   └── daily-progress.md             # Day-by-day engineering log
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

Folders are added **when features arrive** — no empty abstractions.

---

## Design Decisions

### Why a provider interface instead of calling the SDK directly?

The API layer must not know whether the LLM is Groq, OpenAI, Anthropic, or a local model. The `LLMProvider` ABC enforces this at the type level. Adding a new provider is a new file plus a factory branch — no changes to `app/api/`.

### Why Pydantic as the safety boundary?

The LLM is an untrusted component. By validating every response through `BusinessTask`, malformed output becomes a `ValidationError` that the provider wraps into `LLMProviderError`, which the API maps to a clean 502 — never a 500 stack trace, never corrupted state.

### Why does `tenacity` not retry schema errors?

Schema violations are deterministic — the same prompt and model will produce the same invalid output. Retrying wastes tokens, adds latency, and delays surfacing a real bug. Only transient failures (timeouts, 5xx, rate limits) are retried with exponential backoff.

### Why are tests fully mocked?

The plan requires tests to run without a paid or live LLM API. This keeps the suite fast, deterministic, free, and CI-friendly. Live-API smoke tests will be added as a separate, opt-in command later.

---

## Known Limitations

These are honest, current boundaries — not oversights.

- **No database yet.** Persistence arrives on Day 10 (PostgreSQL).
- **No RAG yet.** Retrieval arrives on Days 8–9 (Qdrant or pgvector).
- **No agent loop yet.** Day 4 adds the bounded execution loop.
- **No tool execution yet.** `POST /tasks` classifies intent but does not run tools.
- **Sample data only.** No real customer data is used anywhere.
- **Groq free-tier limits, model names, and pricing change.** Verify on the Groq console before relying on them.
- **No authentication yet.** Tenant isolation is introduced on Day 10 and enforced on Day 15.

---

## Roadmap

- **Days 1–2** — Foundation and LLM classification ✅
- **Days 3–7** — Tools, agent loop, state, tests, first milestone
- **Days 8–10** — RAG, persistence, tenant boundaries
- **Days 11–13** — LangGraph, human approval, evaluation
- **Days 14–17** — Production architecture, security, observability, multi-agent trade-offs
- **Days 18–20** — MCP, Docker, final portfolio

Full plan: [`20-DAY AGENTIC AI ENGINEER CHALLENGE.txt`](20-DAY%20AGENTIC%20AI%20ENGINEER%20CHALLENGE.txt)
Daily log: [`docs/daily-progress.md`](docs/daily-progress.md)

---

## Contributing

This is a personal portfolio project built during a structured challenge. Issues and discussions are welcome, but the day-by-day plan takes priority over outside feature requests.

---

## License

No license declared yet. Treat as **all rights reserved** until one is added.