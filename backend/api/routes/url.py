from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from backend.analyzers.url_analyzer import analyze_url

router = APIRouter()

class URLRequest(BaseModel):
    url: str

class URLResponse(BaseModel):
    url: str
    risk_score: int
    verdict: str
    virustotal: dict
    google_safe_browsing: dict

@router.post("/analyze/url")
async def analyze_url_endpoint(request: URLRequest):
    """
    Accepts a URL and returns a full risk analysis.
    """
    try:
        result = await analyze_url(request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))