from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import os
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # ← fixed
JWT_SECRET = os.getenv("JWT_SECRET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, bcrypt__ident="2b")

# Models
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# 1. Register
@router.post("/register")
def register(data: RegisterRequest):
    """Register a new user."""
    try:
        # Check if email already exists
        existing = supabase.table("users").select("*").eq("email", data.email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Email already registered!")

        # Hash the password
        hashed_password = pwd_context.hash(data.password)

        # Save to Supabase
        response = supabase.table("users").insert({
            "username": data.username,
            "email": data.email,
            "password_hash": hashed_password
        }).execute()

        return {
            "message": "Registration successful!",
            "user": {
                "username": data.username,
                "email": data.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Login
@router.post("/login")
def login(data: LoginRequest):
    """Login and get a JWT token."""
    try:
        # Find user by email
        response = supabase.table("users").select("*").eq("email", data.email).execute()
        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid email or password!")

        user = response.data[0]

        # Check password
        if not pwd_context.verify(data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password!")

        # Generate JWT token
        token = jwt.encode(
            {"user_id": user["id"], "username": user["username"]},
            JWT_SECRET,
            algorithm="HS256"
        )

        return {
            "message": "Login successful!",
            "token": token,
            "username": user["username"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))