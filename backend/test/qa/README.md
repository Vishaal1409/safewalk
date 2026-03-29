# SafeWalk — FINAL QA TEST Suite

## Overview
This folder contains all the reusable test scripts used during the SafeWalk QA Final Verification (March 23, 2026). Run these scripts before any release to ensure minimum QA standards.

## Prerequisites
- Backend running: `cd backend && uvicorn src.main:app --reload` (port 8000)
- Frontend running: `cd frontend && streamlit run app.py` (port 8501)
- `curl` and `python3` available in PATH

## Test Scripts

| Script | Purpose | Runtime | When to Run |
|--------|---------|---------|-------------|
| `01_full_stress_test.sh` | Complete 51-test suite (all sections) | ~2 min | Before submission / major release |
| `02_smoke_test.sh` | 7 quick health checks | ~10 sec | Before every commit |
| `03_confirm_spam_test.sh` | Confirm button spam prevention | ~15 sec | After modifying `/confirm` endpoint |
| `04_edge_case_test.sh` | 13 edge case + security tests | ~30 sec | After modifying `/hazards` POST |

## Usage

```bash
# Run all tests
cd safewalk/FINAL_QA_TEST
bash 01_full_stress_test.sh

# Quick pre-commit check
bash 02_smoke_test.sh

# Test spam prevention (optionally pass a specific hazard ID)
bash 03_confirm_spam_test.sh
bash 03_confirm_spam_test.sh "hazard-uuid-here"

# Edge cases and security
bash 04_edge_case_test.sh
```

## Pass Criteria
- **Smoke test**: All 7 tests must pass (exit code 0)
- **Full stress test**: ≥ 90% pass rate for GO verdict
- **Confirm spam**: Exactly 1 accepted, rest blocked
- **Edge cases**: All 13 tests must pass

## Notes
- The full stress test creates test hazards in the DB — consider using a test DB for clean runs
- Scripts use `--max-time` flags to prevent hangs on slow connections
- All scripts exit with non-zero code on failure for CI integration
