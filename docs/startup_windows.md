# SafeWalk Startup Guide (Windows)

This document outlines the steps to start the SafeWalk application natively on Windows.

## Prerequisites
- **Python 3.11+** installed
- A `.env` file at `backend/.env` containing `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and `JWT_SECRET`

## 1. Start the Backend Server (FastAPI)

1. Open a Command Prompt or PowerShell window in the project root.
2. Activate the virtual environment:
   ```cmd
   .venv\Scripts\activate
   ```
3. Navigate to the `backend` directory, install dependencies, and start Uvicorn:
   ```cmd
   cd backend
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

The backend API will start on **`http://localhost:8000`**.  
Swagger API docs are available at **`http://localhost:8000/docs`**.

## 2. Start the Frontend (Static HTML)

1. Open a **new** Command Prompt or PowerShell (keep the backend terminal running).
2. Navigate directly to the `frontend` directory:
   ```cmd
   cd frontend
   ```
3. Serve the static HTML index using Python's built-in HTTP server:
   ```cmd
   python -m http.server 3000
   ```

The frontend map interface will be available at **`http://localhost:3000`**.
