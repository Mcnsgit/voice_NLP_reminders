# app/core/metrics.py
from prometheus_client import Counter, Histogram, Info, Gauge
from fastapi import FastAPI, Request
from typing import Callable
import time


# Define metrics
http_requests_total = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status_code"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],  # Define duration buckets
)

active_users_total = Gauge("active_users_total", "Total number of active users")

tasks_total = Counter("tasks_total", "Total number of tasks", ["status"])

app_info = Info("voice_task_app", "Voice Task Application Information")


async def metrics_middleware(request: Request, call_next: Callable):
    """
    Middleware to track request metrics
    """
    start_time = time.time()

    # Get the route path pattern instead of the actual URL to avoid high cardinality
    route_path = request.url.path
    if request.scope.get("route"):
        route_path = request.scope["route"].path

    try:
        response = await call_next(request)

        # Record request duration and count
        duration = time.time() - start_time
        http_request_duration_seconds.labels(
            method=request.method, endpoint=route_path
        ).observe(duration)

        http_requests_total.labels(
            method=request.method, endpoint=route_path, status_code=response.status_code
        ).inc()

        return response

    except Exception as e:
        # Record failed requests
        http_requests_total.labels(
            method=request.method, endpoint=route_path, status_code=500
        ).inc()
        raise e


def setup_metrics(app: FastAPI) -> None:
    """
    Setup Prometheus metrics for the FastAPI application
    """
    # Add application info
    app_info.info(
        {"version": "1.0.0", "framework": "fastapi", "python_version": "3.9+"}
    )

    # Add middleware for tracking requests
    app.middleware("http")(metrics_middleware)

    # Helper functions for business metrics
    def increment_task_count(status: str):
        tasks_total.labels(status=status).inc()

    def update_active_users(count: int):
        active_users_total.set(count)

    # Make helper functions available in the app state
    app.state.metrics = {
        "increment_task_count": increment_task_count,
        "update_active_users": update_active_users,
    }


# Example usage in other parts of the application:
"""
# In your FastAPI app initialization:
from app.core.metrics import setup_metrics

app = FastAPI()
setup_metrics(app)

# In your task creation endpoint:
@app.post("/tasks/")
async def create_task(task: TaskCreate):
    # ... task creation logic ...
    request.app.state.metrics['increment_task_count']('TODO')
    return task

# In your user service:
async def update_active_users_count():
    count = await get_active_users_count()
    request.app.state.metrics['update_active_users'](count)
"""
