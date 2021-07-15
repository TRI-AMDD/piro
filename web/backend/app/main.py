import uvicorn
import fastapi

from app import api
from app.react import configure_for_react

app = fastapi.FastAPI()
app.include_router(api.router)
configure_for_react(app)


@app.exception_handler(Exception)
def http_exception_handler(request, exc):
    return fastapi.responses.JSONResponse(content={'error_message': str(exc)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
