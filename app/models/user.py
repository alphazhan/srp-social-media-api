from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

# Enum definitions for user roles and statuses


class Role(str, enum.Enum):
    user = "user"  # Regular registered user
    moderator = "moderator"  # Can manage user content
    admin = "admin"  # Full access and platform management


class Status(str, enum.Enum):
    active = "active"  # Can log in and interact
    banned = "banned"  # Blocked from using the platform


# Main User SQLAlchemy model


class User(Base):
    __tablename__ = "users"  # SQL table name

    id = Column(Integer, primary_key=True)  # Auto-incremented user ID

    # User credentials and identity
    username = Column(
        String(50), unique=True, index=True
    )  # Display name / login handle
    email = Column(String(100), unique=True)  # Unique email for login/verification
    full_name = Column(String(100))  # Display name

    hashed_password = Column(
        String(128)
    )  # Encrypted password (hash only — no raw password stored)

    # Profile customization
    bio = Column(Text, default="")  # Optional short bio
    profile_image_url = Column(
        String(255), nullable=True
    )  # Optional avatar image (URL)

    # Metrics and moderation
    total_posts = Column(Integer, default=0)  # Cached post count
    role = Column(Enum(Role), default=Role.user)  # User access level
    status = Column(Enum(Status), default=Status.active)  # Account status

    # Activity tracking
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # Timestamp of registration
    last_active = Column(
        DateTime(timezone=True), nullable=True
    )  # Last login/activity time

    # ORM relationships
    posts = relationship(
        "Post", back_populates="author", cascade="all, delete"
    )  # One-to-many: posts
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete"
    )  # One-to-many: comments
    likes = relationship(
        "Like", back_populates="user", cascade="all, delete"
    )  # One-to-many: likes
