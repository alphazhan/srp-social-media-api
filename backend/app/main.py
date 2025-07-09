# FastAPI app entrypoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import users, auth, posts, comments, likes, admin
from app.utils.dependencies import lifespan
from app.routers import ws

app = FastAPI(
    title="Social Media API",
    description="A FastAPI-based backend for a social media platform.",
    version="1.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

app.include_router(ws.router)

# Allow requests from your frontend (adjust port if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],  # or ["*"] for testing (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(likes.router, tags=["Likes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


def main():
    print("Hello from srp-social-media-api!")


if __name__ == "__main__":
    main()
