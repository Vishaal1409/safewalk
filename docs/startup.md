# SafeWalk Startup Guide

This document outlines the steps to start the SafeWalk application, including running the backend API, the frontend interface, and how they connect.

---

## Prerequisites

- **Python 3.11+** installed
- Project dependencies installed in a virtual environment
- A `.env` file at the project root with `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and `JWT_SECRET`

```bash
# Activate the virtual environment from the project root
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

---

## Option A: Local Development

### 1. Start the Backend Server (FastAPI)

The backend provides the API for hazard data, authentication, safety scoring, and routing.

1. Open a terminal.
2. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```
3. Run the FastAPI development server using `uvicorn`.
   ```bash
   uvicorn src.main:app --reload
   ```
   *The `--reload` flag enables auto-reloading on code changes.*

The backend will start on **`http://localhost:8000`**.  
API docs are available at **`http://localhost:8000/docs`**.

### 2. Start the Frontend (Static HTML)

The frontend is a single-page HTML application (`frontend/index.html`) that communicates with the backend API.

1. Open a **new** terminal (keep the backend running).
2. Navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```
3. Serve the static files with Python's built-in HTTP server:
   ```bash
   python -m http.server 3000
   ```

The frontend will be available at **`http://localhost:3000`**.

### 3. How They Connect

| Service  | URL                      | Purpose                                            |
|----------|--------------------------|----------------------------------------------------|
| Backend  | `http://localhost:8000`  | REST API for hazards, auth, routing, safety scores |
| Frontend | `http://localhost:3000`  | Static HTML/JS UI — makes API calls to the backend |

---

## Option B: Docker Compose

Run both services with a single command:

```bash
docker-compose up --build
```

| Service  | URL                     | Docker Config                     |
|----------|-------------------------|-----------------------------------|
| Backend  | `http://localhost:8000` | `docker/backend.Dockerfile`       |
| Frontend | `http://localhost:80`   | `docker/frontend.Dockerfile` (nginx) |

Nginx automatically proxies `/api/*` requests to the backend container.

To stop:
```bash
docker-compose down
```

---

## Troubleshooting

- **Map doesn't load / API errors** — Ensure the backend terminal is running without errors and `.env` variables are set.
- **Port conflict** — Check for processes using port 8000 or 3000:
  ```bash
  lsof -i :8000
  kill -9 <PID>
  ```
- **Docker issues** — Run `docker-compose logs` to check container output.
