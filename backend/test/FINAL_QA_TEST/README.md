# SafeWalk Final QA Test Suite

This directory contains the complete, automated test suite used to verify the SafeWalk backend API contracts, stress thresholds, and edge case handlers. 

## Prerequisites
Before running any QA scripts, you **must** ensure that:
1. The SafeWalk FastAPI backend is actively running on `http://localhost:8000`.
2. The SafeWalk static HTML frontend is actively running on `http://localhost:3000`.
3. The `.env` file is properly configured with Supabase credentials, as the tests perform live insertions and read queries against the database.
4. Your machine has `curl` installed (native to macOS and most Linux distros).

## The Test Scripts

| Script | Purpose |
|--------|---------|
| `01_full_stress_test.sh` | **The primary verification script.** Runs 40+ rigorous assertions checking API contract rules (HTTP 201), route safety matrix math, volume bursts, bounding boxes, and security. |
| `02_smoke_test.sh` | Lightweight script for just verifying endpoints are awake and responding to basic reads. |
| `03_confirm_spam_test.sh` | Focused security test designed to maliciously spam the `/confirm` endpoint to ensure duplicate upvotes are clamped. |
| `04_edge_case_test.sh` | Explicit tests checking XSS injections (`<script>`), corrupted multipart forms, and out-of-bounds geographic coordinate attempts. |

## How to Run

Tests must be executed from your terminal. We highly recommend running the scripts from the **project root directory** (not inside the QA folder itself) so the tests can parse the necessary environmental boundaries.

```bash
# Example: Running the full suite
bash backend/test/FINAL_QA_TEST/01_full_stress_test.sh
```

## How to Interpret the Results

The scripts output data sequentially in real-time, categorized into major testing blocks:

- `✅ PASS` - The endpoint responded perfectly per spec (e.g., proper HTTP codes, valid JSON schema, filtered arrays).
- `⏸️ BLOCKED` - The feature is known to be intentionally incomplete or deprecated on the backend roadmap.
- `❌ FAIL` - A critical bug or regression was found. The script will halt the summary output and describe exactly what it expected vs what it received.

**End of Run VERDICT:**
At the end of the script execution, a clean summary will evaluate the percentage of tests passed.
- **`🟢 VERDICT: GO`** — Indicates a 100% pass-rate on critical functions. Ready to merge to main. 
- **`🔴 VERDICT: NO-GO`** — Indicates critical API regressions that must be patched in the backend natively. 

> **A Note on Data Volume:** Passing `01_full_stress_test.sh` inserts exactly 16 dummy records into your Supabase deployment each run. Consider wiping dummy data periodically using Supabase Studio if running the test loop concurrently during debugging.
