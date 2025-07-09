from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

# Like model for tracking user likes on posts


class Like(Base):
    __tablename__ = "likes"  # Table name in the database

    id = Column(
        Integer, primary_key=True, index=True
    )  # Optional unique ID for reference/logging

    # Foreign key to the user who liked the post
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Foreign key to the liked post
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    # Auto timestamp when the like was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ORM relationships to enable backref queries
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    # A user can only like a post once (unique constraint on the pair)
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )
