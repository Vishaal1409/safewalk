# SafeWalk Startup Guide (Mac / Linux)

This guide covers two ways to run SafeWalk:
- **Option A** — Local development using a virtual environment (venv)
- **Option B** — Docker Compose (runs everything in containers)

---

## Prerequisites

- **Python 3.13+** — `brew install python` or [python.org](https://www.python.org/downloads/)
- **Git** — `brew install git` or pre-installed on most systems
- A `.env` file at the project root with:
  ```
  SUPABASE_URL=your_supabase_url
  SUPABASE_SECRET_KEY=your_supabase_key
  JWT_SECRET=your_jwt_secret
  ```
  Copy `.env.example` to get started: `cp .env.example .env`

---

## Option A — Local Development (venv)

### 1. Clone the repo and create a virtual environment

```bash
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk

python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt — that means it's active.

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Start the Backend (FastAPI)

```bash
cd backend
uvicorn src.main:app --reload
```

The `--reload` flag auto-restarts the server when you edit code.

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | REST API |
| `http://localhost:8000/docs` | Swagger interactive API docs |

### 4. Start the Frontend (Static HTML)

Open a **new terminal tab** (keep the backend running), then:

```bash
cd frontend
python3 -m http.server 3000
```

The frontend is now available at **`http://localhost:3000`**

### 5. Service URLs

| Service  | URL                      |
|----------|--------------------------|
| Backend  | http://localhost:8000    |
| Frontend | http://localhost:3000    |
| API Docs | http://localhost:8000/docs |

### 6. Stop the servers

Press `Ctrl + C` in each terminal to stop the backend and frontend.

To deactivate the virtual environment when done:
```bash
deactivate
```

---

## Option B — Docker Compose

> **Prerequisites:** Docker Desktop installed — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the repo

```bash
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk
```

### 2. Add your `.env` file

```bash
cp .env.example .env
# Then edit .env and fill in your Supabase and JWT values
```

### 3. Build and start all services

```bash
docker-compose up --build
```

Both services start automatically. You don't need to run the backend and frontend separately.

| Service  | URL                      |
|----------|--------------------------|
| Frontend | http://localhost:80       |
| Backend  | http://localhost:8000    |
| API Docs | http://localhost:8000/docs |

Nginx automatically proxies `/api/*` requests to the backend container.

### 4. Stop containers

```bash
docker-compose down
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn: command not found` | Run `source .venv/bin/activate` first |
| `ModuleNotFoundError` | Run `pip install -r backend/requirements.txt` again |
| Map doesn't load / API errors | Check the backend terminal — verify `.env` values are correct |
| Port conflict on 8000 or 3000 | Run `lsof -i :8000` then `kill -9 <PID>` |
| Docker build fails | Run `docker-compose logs` to see what went wrong |
| Permission denied on `.sh` scripts | Run `chmod +x script.sh` first |
