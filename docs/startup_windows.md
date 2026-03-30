# SafeWalk Startup Guide (Windows)

This guide covers two ways to run SafeWalk on Windows:
- **Option A** — Local development using a virtual environment (venv)
- **Option B** — Docker Compose (runs everything in containers)

---

## Prerequisites

- **Python 3.11+** — [python.org/downloads](https://www.python.org/downloads/)
- **Git** — [git-scm.com](https://git-scm.com/)
- A `.env` file at the project root with:
  ```
  SUPABASE_URL=your_supabase_url
  SUPABASE_SECRET_KEY=your_supabase_key
  JWT_SECRET=your_jwt_secret
  ```

---

## Option A — Local Development (venv)

### 1. Clone and set up the virtual environment

Open **Command Prompt** or **PowerShell** at the project root:

```cmd
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk

python -m venv .venv
.venv\Scripts\activate
```

### 2. Install backend dependencies

```cmd
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Start the Backend (FastAPI)

```cmd
cd backend
uvicorn src.main:app --reload
```

The backend API is now running at **`http://localhost:8000`**  
Swagger docs are at **`http://localhost:8000/docs`**

### 4. Start the Frontend (Static HTML)

Open a **new** Command Prompt / PowerShell window (keep the backend running):

```cmd
cd frontend
python -m http.server 3000
```

The frontend is now available at **`http://localhost:3000`**

### 5. Service URLs

| Service  | URL                      |
|----------|--------------------------|
| Backend  | http://localhost:8000    |
| Frontend | http://localhost:3000    |
| API Docs | http://localhost:8000/docs |

---

## Option B — Docker Compose

> **Prerequisites:** Docker Desktop installed and running — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the repo

```cmd
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk
```

### 2. Add your `.env` file

Create `.env` in the project root (same as shown in prerequisites above).

### 3. Build and start all services

```cmd
docker-compose up --build
```

This starts both backend and frontend in containers automatically.

| Service  | URL                      |
|----------|--------------------------|
| Frontend | http://localhost:80       |
| Backend  | http://localhost:8000    |
| API Docs | http://localhost:8000/docs |

Nginx automatically proxies `/api/*` requests to the backend.

### 4. Stop containers

```cmd
docker-compose down
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn: command not found` | Make sure `.venv\Scripts\activate` was run first |
| Map doesn't load / API errors | Check the backend terminal — verify `.env` values are set |
| Port already in use | Run `netstat -ano \| findstr :8000` and `taskkill /PID <pid> /F` |
| Docker build fails | Run `docker-compose logs` to see what went wrong |
| Docker Desktop not starting | Ensure Windows Subsystem for Linux (WSL2) is enabled |
