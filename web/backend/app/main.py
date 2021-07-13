import uvicorn
import fastapi

from app import api

app = fastapi.FastAPI()
app.include_router(api.router)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
