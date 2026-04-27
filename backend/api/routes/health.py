from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "fraudar-api",
        "timestamp": datetime.utcnow().isoformat()
    }