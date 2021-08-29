import json
import os
from celery import Celery

from .models import RecommendRoutesRequest, RecommendRoutesTask, RecommendRoutesTaskStatus
from .services import recommend_routes_service

app = Celery(__name__)
app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL', "redis://localhost:6379/0"),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', "redis://localhost:6379/0"),

    # https://medium.com/koko-networks/a-complete-guide-to-production-ready-celery-configuration-5777780b3166
    worker_send_task_event=False,
    task_time_limit=60 * 15,
    task_acks_late=True,
    worker_prefetch_multiplier=1
)


@app.task
def recommend_routes_task(request_dict: dict) -> str:
    return recommend_routes_service(RecommendRoutesRequest(**request_dict))


def recommend_routes_task_start(request: RecommendRoutesRequest) -> RecommendRoutesTask:
    celery_task = recommend_routes_task.delay(request.dict())
    return RecommendRoutesTask(
        task_id=celery_task.id,
        status=RecommendRoutesTaskStatus(celery_task.status.lower()),
        request=request,
        result=json.loads(celery_task.result) if celery_task.ready() else None
    )


def recommend_routes_task_result(task_id: str) -> RecommendRoutesTask:
    celery_task = recommend_routes_task.AsyncResult(task_id)
    status = RecommendRoutesTaskStatus(celery_task.status.lower())

    return RecommendRoutesTask(
        task_id=celery_task.id,
        request=None,
        status=status,
        error_message=str(celery_task.result) if status == RecommendRoutesTaskStatus.FAILURE else None,
        result=json.loads(celery_task.result) if status == RecommendRoutesTaskStatus.SUCCESS else None
    )
