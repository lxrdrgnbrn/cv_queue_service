import os
from celery import Celery
from celery.signals import worker_ready
from prometheus_client import start_http_server

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['worker.tasks']
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_pool='solo' 
)

@worker_ready.connect
def start_metrics_server(sender, **kwargs):
    try:
        port = 8001
        start_http_server(port)
        print(f"[Monitoring] Metrics server started on port {port}")
    except Exception as e:
        print(f"[Monitoring] Failed to start metrics server: {e}")