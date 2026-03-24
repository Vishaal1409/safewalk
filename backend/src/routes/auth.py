from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from passlib.context import CryptContext
from jose import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, bcrypt__ident="2b")

# Models
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=254)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        v = v.strip()
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username may only contain letters, numbers, hyphens, and underscores")
        return v

class LoginRequest(BaseModel):
    email: str = Field(..., max_length=254)
    password: str = Field(..., max_length=128)

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

        new_user = response.data[0]

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": new_user["id"],
                "username": new_user["username"],
                "exp": datetime.now(timezone.utc) + timedelta(hours=24)
            },
            JWT_SECRET,
            algorithm="HS256"
        )

        return {
            "message": "Registration successful!",
            "token": token,
            "user": {
                "username": new_user["username"],
                "email": new_user["email"]
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
            {
                "user_id": user["id"],
                "username": user["username"],
                "exp": datetime.now(timezone.utc) + timedelta(hours=24)
            },
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