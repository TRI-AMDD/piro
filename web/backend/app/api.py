import uuid

import fastapi
from starlette.background import BackgroundTasks

from app.models import RecommendRoutesRequest, PlotlyFigureResponse, RecommendRoutesTask
from app.services import route_recommendation_service, create_route_recommendation_task, get_route_recommendation_task

router = fastapi.APIRouter()


@router.post(
    "/api/recommend_routes",
    description="generate recommended routes for given material as a Plotly figure",
    response_model=PlotlyFigureResponse
)
def recommend_routes(request: RecommendRoutesRequest):
    return fastapi.responses.Response(
        content=route_recommendation_service(request).to_json(),
        status_code=201,
        media_type='application/json',
    )


@router.post(
    "/api/recommend_routes_task",
    description="create background task to generate recommended routes",
    response_model=RecommendRoutesTask
)
def recommend_routes(request: RecommendRoutesRequest, background_tasks: BackgroundTasks) -> RecommendRoutesTask:
    task = RecommendRoutesTask(task_id=str(uuid.uuid4()), request=request)
    background_tasks.add_task(create_route_recommendation_task, task)
    return task


@router.get(
    "/api/recommend_routes_task/{task_id}",
    description="retrieve recommended routes for given material as a Plotly figure from task",
    response_model=RecommendRoutesTask
)
def recommend_routes(task_id: str) -> RecommendRoutesTask:
    return get_route_recommendation_task(task_id)
