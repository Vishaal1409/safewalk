#!/bin/bash
# SafeWalk — Quick Smoke Test (Run Before Every Commit)
# Verifies the core API endpoints are responding correctly.
# Usage: bash 02_smoke_test.sh

API="http://127.0.0.1:8000"
PASS=0; FAIL=0

pass() { PASS=$((PASS+1)); echo "  ✅ $1"; }
fail() { FAIL=$((FAIL+1)); echo "  ❌ $1: $2"; }

echo "╔═══════════════════════════════════════╗"
echo "║   SAFEWALK SMOKE TEST (Quick Check)   ║"
echo "╚═══════════════════════════════════════╝"
echo ""

echo "[1] Health check..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$API/")
[ "$CODE" = "200" ] && pass "Health check OK" || fail "Health check" "HTTP $CODE"

echo "[2] Swagger docs..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$API/docs")
[ "$CODE" = "200" ] && pass "Swagger docs OK" || fail "Swagger docs" "HTTP $CODE"

echo "[3] Frontend..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:8501")
[ "$CODE" = "200" ] && pass "Frontend OK" || fail "Frontend" "HTTP $CODE"

echo "[4] GET /hazards..."
RESP=$(curl -s --max-time 5 "$API/hazards")
COUNT=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('count',0))" 2>/dev/null)
[ -n "$COUNT" ] && [ "$COUNT" -ge 0 ] 2>/dev/null && pass "GET /hazards OK ($COUNT hazards)" || fail "GET /hazards" "Bad response"

echo "[5] Safety score..."
SCORE=$(curl -s --max-time 5 "$API/safety-score?latitude=13.05&longitude=80.23" | python3 -c "import json,sys; print(json.load(sys.stdin).get('safety_score','ERR'))" 2>/dev/null)
[ "$SCORE" != "ERR" ] && pass "Safety score OK ($SCORE)" || fail "Safety score" "Bad response"

echo "[6] Filter by type..."
MH=$(curl -s --max-time 5 "$API/hazards?type=manhole" | python3 -c "
import json,sys; d=json.load(sys.stdin)
ok=all(h['type']=='manhole' for h in d['data'])
print(f'{ok}:{d[\"count\"]}')
" 2>/dev/null)
echo "$MH" | grep -q "True" && pass "Filter works ($(echo $MH | cut -d: -f2) manholes)" || fail "Filter" "Wrong types returned"

echo "[7] Auth login rejects bad creds..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -X POST "$API/auth/login" \
  -H "Content-Type: application/json" -d '{"email":"fake@test.com","password":"wrong"}')
[ "$CODE" = "401" ] && pass "Auth rejects bad creds" || fail "Auth" "HTTP $CODE"

echo ""
TOTAL=$((PASS + FAIL))
echo "Results: $PASS/$TOTAL passed"
[ "$FAIL" -eq 0 ] && echo "🟢 All smoke tests passed!" || echo "🔴 $FAIL test(s) failed — investigate before pushing"
exit $FAIL
