import fastapi

from app.models import RecommendRoutesRequest, PlotlyFigureResponse
from app.services import route_recommendation_service

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
