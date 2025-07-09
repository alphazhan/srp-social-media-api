"""
Handles password hashing, JWT token creation/validation,
and the get_current_user() dependency for authenticated routes.
"""

from passlib.context import CryptContext  # Secure password hashing
from datetime import datetime, timedelta
from jose import JWTError, jwt  # For encoding/decoding JWT tokens
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.database.connection import get_db
from app.models.user import User

# Password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Defines how the app extracts token from requests (OAuth2 Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Hash a plaintext password (during registration)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify a password during login (plaintext vs stored hash)
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# Create a JWT access token with expiration
def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()  # Copy claims
    to_encode.update(
        {
            "exp": datetime.utcnow() + expires_delta  # Set expiry time
        }
    )
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


# Decode and verify JWT token, raise 401 if invalid
def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


# FastAPI dependency that:
# - extracts token from Authorization header
# - decodes it
# - fetches and returns the corresponding User from the DB
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    # Decode token and extract user ID
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    # Fetch user from DB using decoded user ID
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    # Raise if user doesn't exist (e.g., deleted account)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
