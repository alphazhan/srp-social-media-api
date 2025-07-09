from sqlalchemy.orm import declarative_base

# Central base class to register all SQLAlchemy models
Base = declarative_base()


# Declared once and imported wherever needed to avoid circular imports
# from app.models.base import Base
