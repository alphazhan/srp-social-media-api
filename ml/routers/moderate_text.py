from fastapi import APIRouter
from pydantic import BaseModel
from services.moderate_text import moderate_text

router = APIRouter(prefix="/ml", tags=["ML Inference"])


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    category: str
    description: str


@router.post("/moderate-text", response_model=ModerationResponse)
async def moderate_text_route(req: ModerationRequest):
    """
    Analyze the input text for potentially harmful content
    and return a moderation category with description.
    """
    result = moderate_text(req.text)
    return result
