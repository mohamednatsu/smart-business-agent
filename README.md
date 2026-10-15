# Smart Business Agent

An evolving Agentic AI project for the 20-Day Agentic AI Engineer Challenge.

## Requirements
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup
```bash
uv sync


---

## 10. Definition of Done — Verification Checklist

| Requirement | How to Verify |
|---|---|
| Repository and folder structure exist | `ls app/ tests/` shows expected files |
| FastAPI app starts locally | `uv run fastapi dev app/main.py` with no errors |
| Health endpoint works | `curl http://127.0.0.1:8000/health` returns 200 JSON |
| Typed Pydantic models exist | `HealthResponse` and `Settings` are typed |
| At least one passing API test | `uv run pytest -v` shows `passed` |
| Lint runs cleanly | `uv run ruff check .` exits 0 |
| README explains setup | A fresh clone can run using only README steps |

### Final verification command sequence

```bash
uv sync
uv run pytest -v
uv run ruff check .
uv run fastapi dev app/main.py
# In another terminal:
curl -s http://127.0.0.1:8000/health | python -m json.tool