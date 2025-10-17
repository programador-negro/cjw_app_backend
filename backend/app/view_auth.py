from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemes import User
from app.jwt_manager import create_token
from app.managers.db_manager import DbManager

auth_view = APIRouter()

@auth_view.post('/auth/signup', tags=['auth'])
async def signup(user: User):
    try:
        # Create database manager instance
        db = DbManager()
        
        # Check if user already exists
        existing_user = db.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = db.create_user(user)
        return JSONResponse(content={"message": "User created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@auth_view.post('/auth/login', tags=['auth'])
async def login(login_data: LoginRequest):
    try:
        # Create database manager instance
        db = DbManager()
        
        # Verify user credentials
        user_auth = db.verify_user(login_data.email, login_data.password)
        if not user_auth:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        token = create_token({"email": user_auth.email, "id": user_auth.id})
        
        # Create user response without password
        user_response = {
            "id": user_auth.id,
            "email": user_auth.email,
            "name": user_auth.name,
            "role": user_auth.role
        }
        
        return JSONResponse(content={
            "token": token,
            "user": user_response
        }, status_code=200)
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e