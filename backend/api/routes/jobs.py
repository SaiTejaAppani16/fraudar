from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.workers.celery_app import celery_app
from backend.workers.tasks import analyze_url_task, analyze_text_task

router = APIRouter()

class URLJobRequest(BaseModel):
    url: str

class TextJobRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

@router.post("/jobs/analyze/url")
def submit_url_job(request: URLJobRequest):
    """
    Submits URL analysis as a background job.
    Returns job_id immediately — client polls /jobs/{job_id} for results.
    """
    task = analyze_url_task.delay(request.url)
    return JobResponse(
        job_id=task.id,
        status="queued",
        message="URL analysis job submitted. Poll /api/v1/jobs/{job_id} for results."
    )

@router.post("/jobs/analyze/text")
def submit_text_job(request: TextJobRequest):
    """
    Submits text analysis as a background job.
    Returns job_id immediately — client polls /jobs/{job_id} for results.
    """
    if not request.text and not request.url:
        raise HTTPException(
            status_code=400,
            detail="Provide either text or url"
        )
    task = analyze_text_task.delay(text=request.text, url=request.url)
    return JobResponse(
        job_id=task.id,
        status="queued",
        message="Text analysis job submitted. Poll /api/v1/jobs/{job_id} for results."
    )

@router.get("/jobs/{job_id}")
def get_job_result(job_id: str):
    """
    Polls the status and result of a submitted job.
    States: PENDING, STARTED, SUCCESS, FAILURE
    """
    task = celery_app.AsyncResult(job_id)

    if task.state == "PENDING":
        return {"job_id": job_id, "status": "pending", "result": None}
    elif task.state == "STARTED":
        return {"job_id": job_id, "status": "processing", "result": None}
    elif task.state == "SUCCESS":
        return {"job_id": job_id, "status": "completed", "result": task.result}
    elif task.state == "FAILURE":
        return {"job_id": job_id, "status": "failed", "result": str(task.info)}
    else:
        return {"job_id": job_id, "status": task.state, "result": None}