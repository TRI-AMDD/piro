import os

import fastapi
from starlette.staticfiles import StaticFiles

from app.settings import Settings


def configure_index(app: fastapi.FastAPI):
    settings = Settings()
    if settings.enable_react:
        react_dir = settings.react_build_dir

        # do the static files particularly for / should be done after all other routes
        app.mount('/', StaticFiles(directory=react_dir, html=True), name='root')
        app.mount('/static', StaticFiles(directory=os.path.join(react_dir, 'static')), name='static')

    else:
        def redirect_docs():
            return fastapi.responses.RedirectResponse('/docs')

        app.add_api_route("/", redirect_docs, methods=['GET'], description='React demo page', include_in_schema=False)
