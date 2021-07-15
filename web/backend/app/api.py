import fastapi

from app.models import RecommendRoutesForm
from app.services import route_recommendation_service

router = fastapi.APIRouter()


@router.post("/api/recommend_routes", description="generated recommended routes for given material", status_code=201)
def recommend_routes(form: RecommendRoutesForm):
    return route_recommendation_service(form).to_json()
