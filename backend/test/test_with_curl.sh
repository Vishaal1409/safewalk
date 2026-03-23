#!/bin/bash

API_URL="http://127.0.0.1:8000/hazards"

echo "========================================="
echo "1. 🔥 Stress Testing — Add Many Hazards"
echo "========================================="
SUCCESS_COUNT=0
for i in {1..25}; do
  LAT=$(awk -v min=13.0 -v max=13.1 'BEGIN{srand(); print min+rand()*(max-min)}')
  LON=$(awk -v min=80.2 -v max=80.3 'BEGIN{srand(); print min+rand()*(max-min)}')
  TYPES=("manhole" "flooding" "no_light" "broken_footpath" "unsafe_area" "no_wheelchair_access")
  TYPE=${TYPES[$RANDOM % ${#TYPES[@]} ]}
  
  # echo "Adding hazard $i..."
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API_URL \
    -F "type=$TYPE" \
    -F "description=Stress test hazard $i" \
    -F "latitude=$LAT" \
    -F "longitude=$LON" \
    -F "reported_by=StressTester")
  
  if [ "$HTTP_STATUS" -eq 200 ]; then
    SUCCESS_COUNT=$((SUCCESS_COUNT+1))
  fi
done
echo "✅ Successfully added $SUCCESS_COUNT / 25 hazards."

echo ""
echo "fetching a hazard ID to confirm..."
HAZARD_ID=$(curl -s -X GET "http://127.0.0.1:8000/hazards" | grep -o '"id":"[^"]*' | head -1 | awk -F'"' '{print $4}')

if [ -n "$HAZARD_ID" ]; then
    echo "Confirming hazard $HAZARD_ID 10 times..."
    for i in {1..10}; do
        curl -s -o /dev/null -X POST "http://127.0.0.1:8000/hazards/$HAZARD_ID/confirm"
    done
    
    # Check the final count
    FINAL_COUNT=$(curl -s -X GET "http://127.0.0.1:8000/hazards" | grep -A 10 "\"id\":\"$HAZARD_ID\"" | grep -o '"confirmed_count":[0-9]*' | head -1)
    echo "✅ Confirmations finished. Final count for this hazard: $FINAL_COUNT"
else
    echo "❌ Failed to fetch a hazard ID for confirmation test."
fi

echo ""
echo "========================================="
echo "2. 🧩 Weird & Edge Case Inputs"
echo "========================================="

echo "-----------------------------------------"
echo "2A — Empty Description"
echo "-----------------------------------------"
curl -s -X POST $API_URL \
  -F "type=manhole" \
  -F "description=   " \
  -F "latitude=13.05" \
  -F "longitude=80.25" \
  -F "reported_by=EdgeTester" | grep -o '"detail":"[^"]*"' || echo "No explicit detail field in response."
echo ""

echo "-----------------------------------------"
echo "2B — Same Location Spam (10 hazards)"
echo "-----------------------------------------"
SPAM_SUCCESS=0
for i in {1..10}; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST $API_URL \
    -F "type=flooding" \
    -F "description=Spam hazard $i" \
    -F "latitude=13.060000" \
    -F "longitude=80.260000" \
    -F "reported_by=Spammer")
    
  if [ "$HTTP_STATUS" -eq 200 ]; then
    SPAM_SUCCESS=$((SPAM_SUCCESS+1))
  fi
done
echo "✅ Added $SPAM_SUCCESS hazards at the exact same location."
echo ""

echo "-----------------------------------------"
echo "2C — Invalid Coordinates"
echo "-----------------------------------------"
echo "Testing Out of bounds (lat: 999, lon: -999):"
curl -s -X POST $API_URL \
  -F "type=no_light" \
  -F "description=Invalid coords" \
  -F "latitude=999" \
  -F "longitude=-999" \
  -F "reported_by=EdgeTester" | grep -o '"detail":"[^"]*"' || echo "No detail field in response."
echo ""

echo "Testing Missing/Text Coordinates (lat: abc):"
curl -s -X POST $API_URL \
  -F "type=no_light" \
  -F "description=Text coords" \
  -F "latitude=abc" \
  -F "longitude=def" \
  -F "reported_by=EdgeTester" | grep -o '"detail":\[' || echo "No validation array found."
echo "Validation failure expected for text input."
echo ""

echo "Testing Invalid Hazard Type (type=alien_attack):"
curl -s -X POST $API_URL \
  -F "type=alien_attack" \
  -F "description=Aliens" \
  -F "latitude=13.05" \
  -F "longitude=80.25" \
  -F "reported_by=EdgeTester" | grep -o '"detail":"[^"]*"' || echo "No explicit detail field."
echo ""

echo "Automated testing completed."
