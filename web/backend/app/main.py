import uvicorn
import fastapi

from app import api
from app.settings import Settings
from app.index import configure_index

app = fastapi.FastAPI(docs_url="/api/docs", openapi_url="/api")
app.include_router(api.router)
configure_index(app)


@app.exception_handler(Exception)
def http_exception_handler(request, exc):
    return fastapi.responses.JSONResponse(content={'error_message': str(exc)}, status_code=500)


if __name__ == '__main__':
    settings = Settings()
    uvicorn.run(app, port=settings.port, host=settings.host)
