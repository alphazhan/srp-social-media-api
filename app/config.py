# Central config
# Load environment variables and provide settings

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


settings = Settings()
