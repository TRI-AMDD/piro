import fastapi

from app.models import RecommendRoutesForm
from app.services import route_recommendation_service

router = fastapi.APIRouter()


@router.get("/")
def read_root():
    return fastapi.responses.RedirectResponse(url='/docs')


@router.post("/api/recommend_routes", description="generated recommended routes for given material", status_code=201)
def recommend_routes(form: RecommendRoutesForm):
    try:
        return route_recommendation_service(form).to_json()
    except Exception as x:
        return fastapi.responses.JSONResponse(content=str(x), status_code=500)
