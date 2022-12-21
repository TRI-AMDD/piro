import inspect

from app.models import RecommendRoutesRequest

from piro.custom_entry import create_custom_entry
from piro.route import SynthesisRoutes


def recommend_routes_service(request: RecommendRoutesRequest) -> str:
    # handle custom entry
    custom_entry = None
    if request.custom_entry_cif_string:
        custom_entry = create_custom_entry(
            request.custom_entry_cif_string, request.custom_entry_formation_energy_per_atom
        )
        request.target_entry_id = custom_entry.entry_id

    elif not request.target_entry_id.startswith("mp"):
        request.target_entry_id = SynthesisRoutes.get_material_id_from_formula(request.target_entry_id)

    #  maybe there's a better way. pull out the corresponding args from the full request
    args_dict = request.dict()
    synthesis_args = inspect.getfullargspec(SynthesisRoutes).args
    synthesis_args_dict = {k: v for k, v in args_dict.items() if k in synthesis_args}
    recommend_routes_args = inspect.getfullargspec(SynthesisRoutes.recommend_routes).args
    recommend_routes_dict = {k: v for k, v in args_dict.items() if k in recommend_routes_args}

    router = SynthesisRoutes(**synthesis_args_dict, custom_target_entry=custom_entry)
    fig = router.recommend_routes(**recommend_routes_dict)
    return fig.to_json()
