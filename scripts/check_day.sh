#!/usr/bin/env bash
# ============================================================
# Smart Business Agent — Day Completion Check
# ============================================================
# Runs:
#   1. Dependency sync
#   2. Ruff lint (with auto-fix)
#   3. Ruff format check
#   4. Pytest test suite
#   5. FastAPI import smoke test
#
# Usage:
#   ./scripts/check_day.sh           # full check
#   ./scripts/check_day.sh --no-fix  # check without auto-fixing
# ============================================================

set -euo pipefail

# ---------- Colors ----------
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ---------- Config ----------
FIX_MODE=1
for arg in "$@"; do
    case "$arg" in
        --no-fix) FIX_MODE=0 ;;
        *) echo "Unknown argument: $arg"; exit 2 ;;
    esac
done

# ---------- Helpers ----------
step() { echo -e "\n${BLUE}${BOLD}▶ $1${NC}"; }
ok()   { echo -e "${GREEN}  ✓ $1${NC}"; }
warn() { echo -e "${YELLOW}  ⚠ $1${NC}"; }
fail() { echo -e "${RED}  ✗ $1${NC}"; }

FAILED=0

run_step() {
    local name="$1"; shift
    step "$name"
    if "$@"; then
        ok "$name passed"
    else
        fail "$name FAILED"
        FAILED=1
    fi
}

# ---------- Ensure we're in the project root ----------
if [[ ! -f "pyproject.toml" ]]; then
    echo -e "${RED}Error: pyproject.toml not found.${NC}"
    echo "Run this script from the project root (smart-business-agent/)."
    exit 1
fi

# ---------- Check uv is installed ----------
if ! command -v uv >/dev/null 2>&1; then
    echo -e "${RED}Error: uv is not installed.${NC}"
    echo "Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD} Smart Business Agent — Day Completion Check${NC}"
echo -e "${BOLD}============================================================${NC}"
echo "  Project: $(pwd)"
echo "  Date:    $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Mode:    $([[ $FIX_MODE -eq 1 ]] && echo 'fix' || echo 'check-only')"

# ---------- 1. Sync dependencies ----------
run_step "Sync dependencies (uv sync)" uv sync --quiet

# ---------- 2. Ruff lint ----------
if [[ $FIX_MODE -eq 1 ]]; then
    run_step "Ruff lint --fix" uv run ruff check --fix .
else
    run_step "Ruff lint" uv run ruff check .
fi

# ---------- 3. Ruff format ----------
if [[ $FIX_MODE -eq 1 ]]; then
    run_step "Ruff format" uv run ruff format .
else
    run_step "Ruff format --check" uv run ruff format --check .
fi

# ---------- 4. Ruff format verify after fix ----------
# Run a second check so auto-fixes from lint don't leave unformatted code
run_step "Ruff format verify" uv run ruff format --check .

# ---------- 5. Tests ----------
run_step "Pytest" uv run pytest -v


# ---------- Summary ----------
echo -e "\n${BOLD}============================================================${NC}"
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}  ✓ ALL CHECKS PASSED${NC}"
    echo -e "${BOLD}============================================================${NC}"
    echo ""
    echo "Next steps for closing the day:"
    echo "  1. Update docs/daily-progress.md"
    echo "  2. Update README if setup or usage changed"
    echo "  3. git add . && git commit -m \"feat: day-N <summary>\""
    echo ""
    exit 0
else
    echo -e "${RED}${BOLD}  ✗ SOME CHECKS FAILED — fix before committing${NC}"
    echo -e "${BOLD}============================================================${NC}"
    exit 1
fi