import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from passlib.context import CryptContext
from typing import Optional

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/cjw_db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    start_date = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

class DbManager:
    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    def create_user(self, user_data: dict) -> Optional[User]:
        """Create a new user"""
        try:
            # Truncate and hash the password
            password = user_data.password.encode('utf-8')[:72].decode('utf-8')
            hashed_password = pwd_context.hash(password)
            
            # Create new user instance
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password=hashed_password,
                role=user_data.role
            )
            
            # Add and commit to database
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return db_user
        except Exception as e:
            self.db.rollback()
            print(f"Error creating user: {e}")
            return None

    def verify_user(self, email: str, password: str) -> Optional[User]:
        """Verify user credentials"""
        try:
            # Get user by email
            user = self.get_user_by_email(email)
            if not user:
                print("User not found")
                return None
            
            try:
                # Truncate password to 72 bytes as per bcrypt limitation
                password = password.encode('utf-8')[:72].decode('utf-8')
                
                # Verify password
                if not pwd_context.verify(password, user.password):
                    print("Invalid password")
                    return None
                
                return user
            except Exception as ve:
                print(f"Password verification error: {ve}")
                return None
                
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None

    def get_all_users(self):
        """Get all users"""
        try:
            return self.db.query(User).all()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []