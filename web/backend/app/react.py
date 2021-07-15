import os

import fastapi
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


def configure_for_react(app: fastapi.FastAPI):
    react_dir = os.environ.get('REACT_BUILD_DIR', os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        'frontend',
        'build'
    ))

    # add routes for any multi-page endpoints
    templates = Jinja2Templates(react_dir)

    def serve_index(request: Request):
        return templates.TemplateResponse('/index.html', {'request': request})

    app.add_api_route("/demo", serve_index, methods=['GET'], description='React demo page', include_in_schema=False)

    # do the static files particularly for / should be done after all other routes
    app.mount('/', StaticFiles(directory=react_dir, html=True), name='root')
    app.mount('/static', StaticFiles(directory=os.path.join(react_dir, 'static')), name='static')

