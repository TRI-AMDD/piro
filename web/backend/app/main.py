import os

import uvicorn
import fastapi
from starlette.staticfiles import StaticFiles

from app import api

app = fastapi.FastAPI()
app.include_router(api.router)

# for serving React app
react_dir = os.environ.get('REACT_BUILD_DIR', '../../frontend/build')
app.mount('/', StaticFiles(directory=react_dir, html=True), name='root')
app.mount('/static', StaticFiles(directory=os.path.join(react_dir, 'static')), name='static')


@app.exception_handler(Exception)
def http_exception_handler(request, exc):
    return fastapi.responses.JSONResponse(content={'error_message': str(exc)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
