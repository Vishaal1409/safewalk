# SafeWalk API Documentation

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### 1. Health Check
**GET** `/`

Example Response:
```json
{
  "status": "online",
  "message": "SafeWalk Backend is active!"
}
```

---

### 2. Get Hazards
**GET** `/hazards`

Optional Parameters:
| Parameter | Type | Description |
|---|---|---|
| latitude | float | Filter by location |
| longitude | float | Filter by location |
| radius | float | Search radius in degrees (default 0.01 ≈ 1km) |

Example Response:
```json
{
  "status": "success",
  "message": "Hazards fetched successfully",
  "data": [
    {
      "id": "abc123",
      "type": "manhole",
      "description": "Open manhole near bus stop",
      "latitude": 13.0827,
      "longitude": 80.2707,
      "photo_url": null,
      "reported_by": "arun",
      "confirmed_count": 2,
      "created_at": "2026-03-13T10:00:00"
    }
  ],
  "count": 1
}
```

---

### 3. Report a Hazard
**POST** `/hazards`

Form Data:
| Field | Type | Required | Description |
|---|---|---|---|
| type | string | ✅ | One of: manhole, flooding, no_light, broken_footpath, unsafe_area, no_wheelchair_access |
| description | string | ✅ | Description of the hazard |
| latitude | float | ✅ | Must be between -90 and 90 |
| longitude | float | ✅ | Must be between -180 and 180 |
| reported_by | string | ✅ | Name of the reporter |
| image | file | ❌ | Optional photo (JPG or PNG) |

Example Response:
```json
{
  "status": "success",
  "message": "Hazard reported successfully!",
  "data": [
    {
      "id": "abc123",
      "type": "manhole",
      "description": "Open manhole near bus stop",
      "latitude": 13.0827,
      "longitude": 80.2707,
      "photo_url": "https://supabase.co/storage/...",
      "reported_by": "arun",
      "confirmed_count": 0,
      "created_at": "2026-03-13T10:00:00"
    }
  ]
}
```

Error Responses:
```json
{ "detail": "Invalid hazard type. Allowed types: [...]" }
{ "detail": "Invalid latitude. Must be between -90 and 90" }
{ "detail": "Invalid longitude. Must be between -180 and 180" }
{ "detail": "Description cannot be empty" }
```

---

### 4. Confirm a Hazard
**POST** `/hazards/{hazard_id}/confirm`

URL Parameter:
| Parameter | Type | Description |
|---|---|---|
| hazard_id | string | ID of the hazard to confirm |

Example Response:
```json
{
  "status": "success",
  "message": "Hazard confirmed!",
  "confirmed_count": 3
}
```

---

### 5. Get Safety Score
**GET** `/safety-score`

Parameters:
| Parameter | Type | Required | Description |
|---|---|---|---|
| latitude | float | ✅ | Location latitude |
| longitude | float | ✅ | Location longitude |
| radius | float | ❌ | Search radius (default 0.01) |

Example Response:
```json
{
  "status": "success",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "nearby_hazards_count": 3,
  "safety_score": 92.0,
  "safety_label": "✅ Safe"
}
```

Safety Score Labels:
| Score | Label |
|---|---|
| 80-100 | ✅ Safe |
| 60-79 | ⚠️ Use Caution |
| 40-59 | 🟠 Moderate Risk |
| 0-39 | 🔴 High Risk |

---

### 6. Auth Endpoints

#### Register
**POST** `/auth/register`
```json
{
  "username": "yourname",
  "email": "your@email.com",
  "password": "yourpassword"
}
```

Example Response:
```json
{
  "message": "Registration successful!",
  "user": {
    "username": "yourname",
    "email": "your@email.com"
  }
}
```

#### Login
**POST** `/auth/login`
```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

Example Response:
```json
{
  "message": "Login successful!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "yourname"
}
```