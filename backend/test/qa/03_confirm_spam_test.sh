#!/bin/bash
# SafeWalk — Confirm Spam Prevention Test
# Verifies that the double-confirm bug fix is working.
# Usage: bash 03_confirm_spam_test.sh [HAZARD_ID]

API="http://127.0.0.1:8000"

echo "╔════════════════════════════════════════════╗"
echo "║   SAFEWALK CONFIRM SPAM PREVENTION TEST    ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Get a hazard ID to test with (use argument or fetch first one)
if [ -n "$1" ]; then
  HAZARD_ID="$1"
else
  echo "Fetching a hazard ID..."
  HAZARD_ID=$(curl -s --max-time 5 "$API/hazards" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if d['data']:
    print(d['data'][0]['id'])
" 2>/dev/null)
fi

if [ -z "$HAZARD_ID" ]; then
  echo "❌ No hazard ID found. Add some hazards first."
  exit 1
fi

echo "Testing hazard: $HAZARD_ID"
echo ""

# Get initial count
INIT=$(curl -s --max-time 5 "$API/hazards" | python3 -c "
import json,sys
d=json.load(sys.stdin)
h=[x for x in d['data'] if x['id']=='$HAZARD_ID']
print(h[0]['confirmed_count'] if h else -1)
" 2>/dev/null)
echo "Initial confirmed_count: $INIT"
echo ""

# Generate a unique user for this test run
USER="spam_test_$(date +%s)"

echo "Sending 10 rapid confirmations as '$USER'..."
OK=0; ERR=0
for i in $(seq 1 10); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -X POST "$API/hazards/$HAZARD_ID/confirm?confirmed_by=$USER")
  if [ "$CODE" = "200" ]; then
    OK=$((OK+1))
    echo "  Attempt $i: ✅ 200 (accepted)"
  elif [ "$CODE" = "400" ]; then
    ERR=$((ERR+1))
    echo "  Attempt $i: 🚫 400 (blocked)"
  else
    echo "  Attempt $i: ⚠️  $CODE (unexpected)"
  fi
done

echo ""
echo "Results: $OK accepted, $ERR blocked"

# Check final count
FINAL=$(curl -s --max-time 5 "$API/hazards" | python3 -c "
import json,sys
d=json.load(sys.stdin)
h=[x for x in d['data'] if x['id']=='$HAZARD_ID']
print(h[0]['confirmed_count'] if h else -1)
" 2>/dev/null)
echo "Final confirmed_count: $FINAL (expected: $((INIT+1)))"

if [ "$OK" -eq 1 ] && [ "$ERR" -eq 9 ] && [ "$FINAL" -eq $((INIT+1)) ]; then
  echo ""
  echo "🟢 PASS — Confirm spam prevention is working correctly!"
  echo "  Only 1 confirmation accepted, 9 blocked, DB count incremented by exactly 1."
else
  echo ""
  echo "🔴 FAIL — Spam prevention may not be working correctly."
  echo "  Expected: 1 OK + 9 blocked + count=$((INIT+1))"
  echo "  Got:      $OK OK + $ERR blocked + count=$FINAL"
fi
