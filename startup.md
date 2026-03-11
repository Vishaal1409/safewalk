# SafeWalk Startup Guide

This document outlines the steps to start the SafeWalk application, including running the backend API, the frontend interface, and how they connect.

## Prerequisites

Ensure you have Python 3.x installed and that you have installed all the necessary requirements for both the frontend and backend. 
It's recommended to do this within the virtual environment.

```bash
# Activate the virtual environment from the project root
source .venv/bin/activate
```

## 1. Start the Backend Server (FastAPI)

The backend provides the API for the application and handles database interactions, safety scoring, and routing.

1. Open a terminal.
2. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```
3. Run the FastAPI development server using `uvicorn`. Note that the application instance is located in `src/main.py`.
   ```bash
   uvicorn src.main:app --reload
   ```
   *The `--reload` flag enables auto-reloading when you make code changes.*

The backend will start running on `http://127.0.0.1:8000`. You can view the automatically generated API documentation by visiting `http://127.0.0.1:8000/docs` in your browser.

## 2. Start the Frontend App (Streamlit)

The frontend is a Streamlit application that provides the user interface with the map and hazard reporting features.

1. Open a **new** terminal window (keep the backend server running in the first terminal).
2. Activate your virtual environment in this new terminal if you haven't already.
3. Navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```
4. Run the Streamlit application.
   ```bash
   streamlit run app.py
   ```

Streamlit will start a local web server and typically opens the application in your default web browser automatically at `http://localhost:8501`.

## 3. How They Connect

The connection between the frontend and backend happens automatically over your local network:

1. **Backend**: Runs on port `8000` (`http://localhost:8000`). It listens for incoming HTTP requests (GET, POST, etc.) for hazard data, authentication, and routing.
2. **Frontend**: Runs on port `8501` (`http://localhost:8501`). The Streamlit code (`frontend/app.py` or underlying modules) makes HTTP requests to `http://localhost:8000` to fetch the map data, submit reports, and get route information.

**Troubleshooting Connection Issues**:
- If the map doesn't load or data isn't fetching, ensure the backend terminal is running without errors.
- Ensure no other processes are using port `8000` or `8501`. If the backend fails because port 8000 is occupied, you might need to kill the conflicting process (e.g., `lsof -i :8000` followed by `kill -9 <PID>`).
