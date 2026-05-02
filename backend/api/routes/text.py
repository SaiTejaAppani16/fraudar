from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.analyzers.text_analyzer import analyze_content

router = APIRouter()

class TextRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

@router.post("/analyze/text")
async def analyze_text_endpoint(request: TextRequest):
    """
    Accepts raw text or a URL and returns scam analysis.
    Use for emails, job postings, or any suspicious text content.
    """
    if not request.text and not request.url:
        raise HTTPException(
            status_code=400,
            detail="Provide either text or url in the request body"
        )
    
    try:
        result = await analyze_content(text=request.text, url=request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))