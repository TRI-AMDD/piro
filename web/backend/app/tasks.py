import json

from celery import Celery

from app import celery_config
from app.models import RecommendRoutesRequest, RecommendRoutesTask, RecommendRoutesTaskStatus
from app.services import recommend_routes_service

app = Celery(__name__)
app.config_from_object(celery_config)


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

    if isinstance(celery_task.result, Exception):
        raise celery_task.result

    return RecommendRoutesTask(
        task_id=celery_task.id,
        status=RecommendRoutesTaskStatus(celery_task.status.lower()),
        result=json.loads(celery_task.result) if celery_task.ready() else None
    )
