from plotly.graph_objs import Figure
from piro.route import SynthesisRoutes
from app.models import RecommendRoutesForm


def route_recommendation_service(form: RecommendRoutesForm) -> Figure:
    if not form.mp_id.startswith("mp"):
        form.mp_id = SynthesisRoutes.get_material_id_from_formula(form.mp_id)

    router = SynthesisRoutes(form.mp_id, add_elements=form.add_elements, use_cache_database=False)
    fig = router.recommend_routes(
        temperature=form.temperature,
        pressure=form.pressure,
        max_component_precursors=form.max_component_precursors,
        **form.synthesis_bool_options.dict()
    )
    return fig
