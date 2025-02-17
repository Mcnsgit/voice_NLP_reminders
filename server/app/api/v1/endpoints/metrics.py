# app/api/v1/endpoints/metrics.py
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


router = APIRouter()


@router.get("/metrics", response_class=PlainTextResponse)
# @require_superuser
async def get_metrics():
    """
    Get Prometheus metrics. Only accessible by superusers.
    """
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
