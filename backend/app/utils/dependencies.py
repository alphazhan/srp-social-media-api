# Shared dependencies like `require_admin()` or `lifespan` logic

from fastapi import Depends, HTTPException
from app.models.user import User
from app.utils.security import get_current_user


# Dependency that ensures the current user has admin privileges.
def require_admin(current_user: User = Depends(get_current_user)):
    # Check user's role; deny access if not admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user  # Return user object if role is valid


# Lifespan event handler to run during app startup
# Used by FastAPI to run initialization logic (e.g. DB setup)
async def lifespan(app):
    from app.database.connection import init_db

    await init_db()  # Create tables on app startup (safe for dev/local)
    yield  # Keeps the app running until shutdown
