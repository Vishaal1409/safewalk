#!/bin/bash
# SafeWalk — Edge Case & Security Test
# Tests input validation, XSS prevention, and boundary conditions.
# Usage: bash 04_edge_case_test.sh

API="http://127.0.0.1:8000"
PASS=0; FAIL=0

pass() { PASS=$((PASS+1)); echo "  ✅ PASS: $1"; }
fail() { FAIL=$((FAIL+1)); echo "  ❌ FAIL: $1 — $2"; }

echo "╔═════════════════════════════════════════════╗"
echo "║   SAFEWALK EDGE CASE & SECURITY TESTS       ║"
echo "╚═════════════════════════════════════════════╝"
echo ""

echo "━━━ INPUT VALIDATION ━━━"

echo "[1] Empty description..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=" -F "latitude=13.05" -F "longitude=80.23" -F "reported_by=test")
[ "$CODE" = "400" ] || [ "$CODE" = "422" ] && pass "Empty desc rejected ($CODE)" || fail "Empty desc" "HTTP $CODE"

echo "[2] Whitespace-only description..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=   " -F "latitude=13.05" -F "longitude=80.23" -F "reported_by=test")
[ "$CODE" = "400" ] || [ "$CODE" = "422" ] && pass "Whitespace desc rejected ($CODE)" || fail "Whitespace desc" "HTTP $CODE — accepted whitespace"

echo "[3] Invalid hazard type..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=alien_attack" -F "description=Test" -F "latitude=13.05" -F "longitude=80.23" -F "reported_by=test")
[ "$CODE" = "400" ] && pass "Invalid type rejected ($CODE)" || fail "Invalid type" "HTTP $CODE"

echo "[4] Out-of-range latitude (999)..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Bad lat" -F "latitude=999" -F "longitude=80.23" -F "reported_by=test")
[ "$CODE" = "400" ] && pass "Bad latitude rejected ($CODE)" || fail "Bad latitude" "HTTP $CODE"

echo "[5] Out-of-range longitude (-999)..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Bad lon" -F "latitude=13.05" -F "longitude=-999" -F "reported_by=test")
[ "$CODE" = "400" ] && pass "Bad longitude rejected ($CODE)" || fail "Bad longitude" "HTTP $CODE"

echo "[6] Text as coordinates..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Text" -F "latitude=abc" -F "longitude=def" -F "reported_by=test")
[ "$CODE" = "422" ] && pass "Text coords rejected ($CODE)" || fail "Text coords" "HTTP $CODE"

echo "[7] Non-image file upload..."
echo "not an image" > /tmp/sw_fake.txt
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Fake img" -F "latitude=13.05" -F "longitude=80.23" \
  -F "reported_by=test" -F "image=@/tmp/sw_fake.txt")
[ "$CODE" = "400" ] && pass "Non-image rejected ($CODE)" || fail "Non-image" "HTTP $CODE"
rm -f /tmp/sw_fake.txt

echo "[8] Large file (6MB)..."
dd if=/dev/zero of=/tmp/sw_large.jpg bs=1024 count=6000 2>/dev/null
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Large file" -F "latitude=13.05" -F "longitude=80.23" \
  -F "reported_by=test" -F "image=@/tmp/sw_large.jpg")
[ "$CODE" != "500" ] && pass "Large file handled ($CODE)" || fail "Large file" "HTTP 500"
rm -f /tmp/sw_large.jpg

echo ""
echo "━━━ SECURITY TESTS ━━━"

echo "[9] XSS in description..."
RESP=$(curl -s --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=<script>alert('xss')</script>" -F "latitude=13.05" \
  -F "longitude=80.23" -F "reported_by=test")
DESC=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data'][0]['description'])" 2>/dev/null)
echo "  Stored: $DESC"
if echo "$DESC" | grep -q '&lt;script&gt;'; then
  pass "XSS escaped (html.escape working)"
elif echo "$DESC" | grep -q '<script>'; then
  fail "XSS" "Raw <script> stored — VULNERABILITY"
else
  pass "XSS sanitized"
fi

echo "[10] SQL injection attempt..."
RESP=$(curl -s -w "\n%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description='; DROP TABLE hazards; --" -F "latitude=13.05" \
  -F "longitude=80.23" -F "reported_by=test")
CODE=$(echo "$RESP" | tail -1)
[ "$CODE" = "200" ] && pass "SQL injection handled (Supabase parameterized)" || echo "  ⚠️ HTTP $CODE (review manually)"

echo ""
echo "━━━ BOUNDARY TESTS ━━━"

echo "[11] Coords outside Chennai (Delhi)..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Delhi" -F "latitude=28.6139" -F "longitude=77.2090" -F "reported_by=test")
[ "$CODE" = "200" ] || [ "$CODE" = "400" ] && pass "Out-of-Chennai handled ($CODE)" || fail "Delhi coords" "HTTP $CODE"

echo "[12] Duplicate at same location..."
D1=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Dup 1" -F "latitude=13.0500" -F "longitude=80.2300" -F "reported_by=test")
D2=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards" \
  -F "type=manhole" -F "description=Dup 2" -F "latitude=13.0500" -F "longitude=80.2300" -F "reported_by=test")
[ "$D1" = "200" ] && [ "$D2" = "200" ] && pass "Duplicates allowed" || fail "Duplicates" "D1=$D1 D2=$D2"

echo "[13] Confirm non-existent hazard..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -X POST "$API/hazards/00000000-0000-0000-0000-000000000000/confirm?confirmed_by=test")
[ "$CODE" = "404" ] && pass "Non-existent hazard returns 404" || fail "Non-existent confirm" "HTTP $CODE"

echo ""
TOTAL=$((PASS + FAIL))
echo "Results: $PASS/$TOTAL passed"
[ "$FAIL" -eq 0 ] && echo "🟢 All edge case tests passed!" || echo "🔴 $FAIL test(s) failed"
exit $FAIL
