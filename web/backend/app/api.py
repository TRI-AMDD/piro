import fastapi

from .models import RecommendRoutesRequest, PlotlyFigureResponse, RecommendRoutesTask
from .services import recommend_routes_service
from .tasks import recommend_routes_task_start, recommend_routes_task_result

router = fastapi.APIRouter()


@router.post(
    "/api/recommend_routes",
    description="generate recommended routes for given material as a Plotly figure",
    response_model=PlotlyFigureResponse
)
def recommend_routes(request: RecommendRoutesRequest):
    return fastapi.responses.Response(
        content=recommend_routes_service(request),
        status_code=201,
        media_type='application/json',
    )


@router.post(
    "/api/recommend_routes_task",
    description="create background task to generate recommended routes",
    response_model=RecommendRoutesTask
)
def recommend_routes(request: RecommendRoutesRequest) -> RecommendRoutesTask:
    return recommend_routes_task_start(request)


@router.get(
    "/api/recommend_routes_task/{task_id}",
    description="retrieve recommended routes for given material as a Plotly figure from task",
    response_model=RecommendRoutesTask
)
def recommend_routes(task_id: str) -> RecommendRoutesTask:
    return recommend_routes_task_result(task_id)
