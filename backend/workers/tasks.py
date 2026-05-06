from backend.workers.celery_app import celery_app
from backend.analyzers.url_analyzer import analyze_url
from backend.analyzers.text_analyzer import analyze_content
import asyncio

@celery_app.task(bind=True, max_retries=3)
def analyze_url_task(self, url: str):
    """
    Async Celery task for URL analysis.
    Runs in background worker — doesn't block the API server.
    max_retries=3 means if it fails, it retries 3 times automatically.
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(analyze_url(url))
        loop.close()
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def analyze_text_task(self, text: str = None, url: str = None):
    """
    Async Celery task for text/content analysis.
    Runs in background worker — doesn't block the API server.
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(analyze_content(text=text, url=url))
        loop.close()
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)