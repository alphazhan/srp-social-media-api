from fastapi import APIRouter
from pydantic import BaseModel
from services.extract_hashtags import extract_hashtags

router = APIRouter(prefix="/ml", tags=["ML Inference"])


class HashtagRequest(BaseModel):
    text: str


class HashtagResponse(BaseModel):
    hashtags: list[str]


@router.post("/extract-hashtags", response_model=HashtagResponse)
async def extract_hashtags_route(req: HashtagRequest):
    """
    Generate relevant hashtags from the provided input text.
    """
    tags = extract_hashtags(req.text)
    return {"hashtags": tags}
