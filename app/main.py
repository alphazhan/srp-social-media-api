# FastAPI app entrypoint
from fastapi import FastAPI
from app.routers import users, auth, posts, comments, likes, admin
from app.utils.dependencies import lifespan

app = FastAPI(
    title="Social Media API",
    description="A FastAPI-based backend for a social media platform.",
    version="1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


def main():
    print("Hello from srp-social-media-api!")


if __name__ == "__main__":
    main()
