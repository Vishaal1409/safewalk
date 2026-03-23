# 🧪 QA & Real-World Testing Guide
### Tester: Arun | Role: QA Engineer
> **Goal:** Stress test the hazard reporting system, uncover edge cases, validate performance, and deliver a structured bug report.

---

## 📋 Table of Contents
1. [Stress Testing — Add Many Hazards](#1-stress-testing--add-many-hazards)
2. [Weird & Edge Case Inputs](#2-weird--edge-case-inputs)
3. [Performance Check](#3-performance-check)
4. [Final Bug Report Template](#4-final-bug-report-template)

---

## 1. 🔥 Stress Testing — Add Many Hazards

### Objective
Flood the system with a high volume of hazard entries to check for crashes, slowdowns, data loss, or UI breakage.

### Instructions

#### Step 1 — Rapid Hazard Entry
- Add a minimum of **20–30 hazards** back-to-back without refreshing the page.
- Use a mix of all available hazard types (e.g., flood, fire, accident, obstruction, etc.).
- Vary the locations across the map — don't cluster everything in one area initially.

#### Step 2 — Confirm Many Times
- After adding hazards, use the **"Confirm"** button on as many reports as possible.
- Try confirming the same hazard **5–10 times in a row** and note the behaviour.
- Check if the confirmation count increments correctly or caps/breaks.

#### Step 3 — Observe System Behaviour
During and after the stress test, check and note:

| Check | Expected | Observed |
|-------|----------|----------|
| UI remains responsive | ✅ No freeze | |
| All hazards appear on map | ✅ All pins visible | |
| Data persists after adding 30+ entries | ✅ No data loss | |
| Confirm count updates correctly | ✅ Increments per click | |
| No duplicate markers overlapping strangely | ✅ Clean clustering | |
| Console shows no JS errors | ✅ Error-free | |

> 💡 **Tip:** Open browser DevTools (`F12` → Console) while testing to catch silent errors.

---

## 2. 🧩 Weird & Edge Case Inputs

### Objective
Test the system's resilience against invalid, unusual, or malicious inputs.

---

### 2A — Empty Description

**Test Steps:**
1. Click to add a new hazard.
2. Leave the **description field completely blank**.
3. Fill in all other fields normally and submit.

**What to Check:**
- Does the system accept or reject the empty submission?
- Is there a validation message shown to the user?
- Does a blank-description hazard appear on the map?
- Does it break anything downstream (e.g., popup display, filtering)?

**Expected Behaviour:** Form should either reject empty description with a clear error, or handle it gracefully with a placeholder like *"No description provided."*

---

### 2B — Same Location Spam

**Test Steps:**
1. Add **10 or more hazards** at the exact same GPS coordinates or by clicking the same spot on the map.
2. Use different hazard types and descriptions each time.
3. Also try: same location AND same type AND same description — pure duplicate.

**What to Check:**
- Do markers stack invisibly on top of each other?
- Does the clustering algorithm handle the pile-up cleanly?
- Is there any duplicate detection or merge logic?
- Can you still click and view all overlapping hazards?

**Expected Behaviour:** Clustering should group same-location markers. A click should reveal all entries at that point.

---

### 2C — Invalid Coordinates

**Test Steps:**
1. If the system has manual coordinate input, try:
   - Latitude: `999`, `-999`, `0`, `91`, `-91`
   - Longitude: `999`, `-999`, `0`, `181`, `-181`
2. Try submitting with coordinates **outside India** (or outside the expected map bounds).
3. Try entering **text instead of numbers** in coordinate fields (e.g., `"abc"`, `"!@#"`).
4. Try **null / blank** coordinate fields.

**What to Check:**
- Does the system validate coordinate ranges?
- Does a marker get placed incorrectly on the map?
- Does the app crash or throw an unhandled error?
- Is there a user-facing error message?

**Expected Behaviour:** System should reject out-of-range or non-numeric coordinates with a clear validation error.

---

### 2D — Additional Edge Cases *(Bonus)*

| Input Type | Test Action | Watch For |
|------------|-------------|-----------|
| Very long description | Paste 2000+ characters into description | UI overflow, truncation, crash |
| Special characters | `<script>alert('xss')</script>` in description | XSS vulnerability, escaped output |
| Emoji in fields | Add 🔥🚨💥 to description | Encoding errors, broken display |
| Rapid double-click submit | Click submit button twice very fast | Duplicate entry creation |
| Back button after submit | Add hazard → press browser back → resubmit | Duplicate hazard added again |

---

## 3. ⚡ Performance Check

### Objective
Evaluate map responsiveness and clustering behaviour under load.

---

### 3A — Map Lag Test

**Test Steps:**
1. With **30+ hazards** on the map, perform the following actions and time them mentally:
   - Zoom in and out rapidly (use scroll wheel or buttons)
   - Pan across the map in all directions
   - Switch between hazard type filters
   - Open and close multiple hazard popups

**Rating Scale:**

| Experience | Rating |
|------------|--------|
| Instant, no delay | ✅ Smooth |
| Slight hesitation (< 0.5s) | ⚠️ Acceptable |
| Noticeable lag (0.5s – 2s) | 🔶 Degraded |
| Freezing or unresponsive (> 2s) | ❌ Broken |

---

### 3B — Clustering Quality Check

**Test Steps:**
1. Zoom out to see the full map with all hazards loaded.
2. Gradually zoom in and out and observe clustering behaviour.

**What to Check:**
- Do nearby markers cluster into numbered groups?
- Do clusters **split correctly** as you zoom in?
- Does clicking a cluster zoom into its members cleanly?
- Are cluster counts accurate (e.g., a cluster showing "5" actually contains 5 hazards)?
- At max zoom, do all individual markers display correctly without overlapping?

**Expected Behaviour:** Smooth cluster expand/collapse. No phantom clusters. Accurate counts.

---

### 3C — Filter & Search Performance

- Apply each hazard type filter with 30+ entries loaded.
- Check: Does filtering feel instant or slow?
- Check: Do filtered results update the map markers correctly?
- Check: Are there any hazards that disappear when they shouldn't, or appear when they shouldn't?

---

## 4. 🚨 Where the App Failed (Summary)

Based on the testing, here are the main areas where the application either crashed, behaved incorrectly, or showed vulnerabilities:

1. **Map Filtering Logic**: The "Filter by Type" dropdown and "Confirmed Only" checkbox in the UI do not successfully update the map markers when toggled. The state change isn't triggering a map re-render with filtered data.
2. **Dashboard Statistics**: The summary statistics (Safety Score, Hazards count, Confirmed count) display global totals and do not react to the user applying filters on the map.
3. **Security (Input Validation)**: The hazard description field is vulnerable to Stored Cross-Site Scripting (XSS). It accepts HTML and JavaScript tags without any sanitization before saving to the database.
4. **Abuse Prevention**: The "Confirm" button on hazard popups has no rate limiting or session locking. A single user can repeatedly click confirm to artificially inflate a hazard's confirmation count infinitely.

---

## 5. 📝 Final Bug Report

### Instructions
For every issue found during testing, fill in one row of the table below.

**Severity Key:**
- 🔴 **Critical** — System crash, data loss, security issue
- 🟠 **High** — Core feature broken, no workaround
- 🟡 **Medium** — Feature works but behaves incorrectly
- 🟢 **Low** — Minor UI/UX issue, cosmetic

---

### Bug Report Table

| # | Severity | Area | Bug / Issue Description | Steps to Reproduce | Fix Suggestion |
|---|----------|------|-------------------------|--------------------|----------------|
| 1 | 🟠 High | Map Filters | Filtering by Hazard Type does not update map markers or summary stats. | 1. Select 'Flooding' in dropdown. 2. Observe map markers remain unchanged. | Fix Streamlit state/callback to correctly trigger map re-render and filter dataframe. |
| 2 | 🟡 Medium | UI Features | Checkbox state for "Confirmed Only" does not reliably apply filters on the map. | 1. Toggle Confirmed Only checkbox. 2. Check map. | Ensure checkbox value updates the filter logic in the app. |
| 3 | 🟡 Medium | Abuse Protection | Hazard confirm button lacks rate limiting or session locking. | 1. Click Confirm 10 times rapidly on a hazard. | Prevent multiple confirmations from the same session/IP. |
| 4 | 🟢 Low | Summary Stats | Dashboard summary stats show global total rather than filtered view. | 1. Apply a filter. 2. Look at 'Hazards' count card. | Recalculate summary metrics based on the filtered dataframe. |
| 5 | 🟠 High | Security/Backend | Description field accepts HTML/JS tags without sanitization, leading to potential stored XSS. | 1. Send POST request with description `<script>alert('xss')</script>`. | Implement input sanitization on the backend before saving to Supabase. |

> 📌 Add as many rows as needed. No limit.

---

### Bug Report Example (filled)

| # | Severity | Area | Bug / Issue Description | Steps to Reproduce | Fix Suggestion |
|---|----------|------|-------------------------|--------------------|----------------|
| 1 | 🟠 High | Form Validation | Empty description is accepted and creates a hazard with blank popup content | 1. Open add form. 2. Leave description blank. 3. Submit. | Add required field validation; show inline error "Description cannot be empty" |
| 2 | 🟡 Medium | Clustering | Cluster count shows "6" but only 4 markers appear on zoom-in | 1. Add 6 hazards near each other. 2. Zoom out. 3. Click cluster. | Investigate cluster data sync; ensure all markers are passed to clustering library |
| 3 | 🟢 Low | UI | Confirm button can be clicked 50+ times with no cap or feedback | 1. Add hazard. 2. Click Confirm rapidly 50 times. | Cap confirmations per user session or show "Already confirmed" after first click |

---

## ✅ Testing Completion Checklist

Before submitting your report, confirm:

- [x] 20+ hazards added successfully
- [x] Confirm button tested repeatedly
- [x] Empty description tested
- [x] Same-location spam tested
- [x] Invalid coordinates tested
- [x] Special character / XSS input tested
- [x] Map zoom & pan tested with full load
- [x] Clustering zoom-in/out tested
- [x] All filters tested
- [x] Bug report table completed with fix suggestions
- [x] Browser console checked for errors

---

*Document prepared for QA cycle | Tester: Arun | System: Hazard Reporting Platform*
