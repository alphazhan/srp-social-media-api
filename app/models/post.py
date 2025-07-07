from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

# Post model for user-generated content (text/image posts)


class Post(Base):
    __tablename__ = "posts"  # Name of the table in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for each post

    # Required textual content of the post (e.g., tweet, message, caption)
    content = Column(Text, nullable=False)

    # Optional image (stored elsewhere, referenced via URL)
    image_url = Column(String(255), nullable=True)

    # Reference to the author of this post
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Created at timestamp — auto-generated when inserted
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Updated at timestamp — set automatically if edited
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ORM relationships (for reverse access)
    author = relationship("User", back_populates="posts")  # post.author → User object
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete"
    )  # post.comments → list[Comment]
    likes = relationship(
        "Like", back_populates="post", cascade="all, delete"
    )  # post.likes → list[Like]
