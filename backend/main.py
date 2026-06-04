from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.health import router as health_router
from backend.api.routes.url import router as url_router
from backend.api.routes.text import router as text_router
from backend.api.routes.jobs import router as jobs_router
from backend.rag.rag_pipeline import initialize_rag

app = FastAPI(
    title="Fraudar API",
    description="Real-time scam and fraud detection platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fraudar.onrender.com",
        "https://fraudar-api.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    initialize_rag()

app.include_router(health_router, prefix="/api/v1")
app.include_router(url_router, prefix="/api/v1")
app.include_router(text_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "service": "Fraudar",
        "version": "1.0.0",
        "status": "running"
    }