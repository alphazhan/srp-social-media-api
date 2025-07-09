# Central config
# Load environment variables and provide settings

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # Database connection string
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

    # JWT security config
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    # ML service URL
    ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8001")

    # Frontend URL for CORS
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


settings = Settings()
