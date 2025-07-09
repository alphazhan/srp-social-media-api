from fastapi import APIRouter
from pydantic import BaseModel
from ml.services.detect_language import detect_language

router = APIRouter(prefix="/ml", tags=["ML Inference"])

class LanguageRequest(BaseModel):
    text: str

class LanguageResponse(BaseModel):
    language: str

@router.post("/detect-language", response_model=LanguageResponse)
async def detect_language_route(req: LanguageRequest):
    return {"language": detect_language(req.text)}
