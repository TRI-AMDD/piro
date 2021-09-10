import cProfile
import inspect
import json
import time
from pathlib import Path

import pytest

from piro.route import SynthesisRoutes


requests = json.load(open(Path(__file__).parent / 'example_requests.json'))


@pytest.fixture
def ensure_results_dir():
    results_dir = Path(__file__).parent / 'profiles'
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


@pytest.mark.parametrize("compound", requests.keys())
def test_recommend_routes(ensure_results_dir, compound):
    #  maybe there's a better way. pull out the corresponding args from the full request
    args_dict = requests[compound]
    synthesis_args = inspect.getfullargspec(SynthesisRoutes).args
    synthesis_args_dict = {k: v for k, v in args_dict.items() if k in synthesis_args}
    recommend_routes_args = inspect.getfullargspec(SynthesisRoutes.recommend_routes).args
    recommend_routes_args_dict = {k: v for k, v in args_dict.items() if k in recommend_routes_args}

    def profile_this():
        start_time = time.time()
        router = SynthesisRoutes(**synthesis_args_dict)
        route_start_time = time.time()
        router.recommend_routes(**recommend_routes_args_dict)
        print(f'{compound} took {time.time() - start_time} total, {time.time() - route_start_time} recommend_routes')

    cProfile.runctx('profile_this()', globals(), locals(), str(ensure_results_dir / f'{compound}.prof'))
