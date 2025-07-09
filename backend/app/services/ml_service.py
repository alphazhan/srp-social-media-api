# Service functions for calling the ML microservice

import httpx
from app.config import settings

# Set a longer timeout: 30s total, 5s for connection establishment
TIMEOUT = httpx.Timeout(30.0, connect=5.0)


async def detect_language(text: str) -> str:
    """
    Calls the ML service to detect language from the input text.
    Returns the language label (e.g., 'Kazakh').
    """
    url = f"{settings.ML_SERVICE_URL}/ml/detect-language"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(url, json={"text": text})
        response.raise_for_status()
        return response.json()["language"]


async def extract_hashtags(text: str) -> list[str]:
    """
    Calls the ML service to extract hashtags from the input text.
    Returns a list of hashtag strings.
    """
    url = f"{settings.ML_SERVICE_URL}/ml/extract-hashtags"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(url, json={"text": text})
        response.raise_for_status()
        return response.json()["hashtags"]


async def moderate_text(text: str) -> dict:
    """
    Calls the ML service to check if the input text is appropriate.
    Returns a dictionary with 'category' and 'description'.
    """
    url = f"{settings.ML_SERVICE_URL}/ml/moderate-text"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(url, json={"text": text})
        response.raise_for_status()
        return response.json()
