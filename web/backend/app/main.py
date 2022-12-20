import fastapi
import uvicorn
from app import api
from app.index import configure_index
from app.settings import settings
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

app = fastapi.FastAPI(docs_url="/api/docs", openapi_url="/api")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)
configure_index(app)


@app.middleware("http")
async def no_cache(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.exception_handler(Exception)
def http_exception_handler(request, exc):
    return fastapi.responses.JSONResponse(content={"error_message": str(exc)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, port=settings.port, host=settings.host)
