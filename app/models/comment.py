from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

# Comment model for user-generated replies under posts


class Comment(Base):
    __tablename__ = "comments"  # Table name in the database

    id = Column(Integer, primary_key=True)  # Unique ID for each comment
    text = Column(Text, nullable=False)  # Body content of the comment

    # Link to the post that this comment belongs to
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    # Link to the user who wrote this comment
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Automatically set timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ORM relationships
    post = relationship(
        "Post", back_populates="comments"
    )  # Reverse access: post.comments
    user = relationship(
        "User", back_populates="comments"
    )  # Reverse access: user.comments
