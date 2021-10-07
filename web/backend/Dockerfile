FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim as api
# this image is setup to run fastapi via gunicorn
# reference for how to use the image https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
# this should be built from root of repo

RUN apt-get update && apt-get install gcc -y && rm -rf /var/lib/apt/lists/*

# python requirements
COPY web/backend/requirements.txt /app/web/backend/requirements.txt
RUN pip3 install --no-cache-dir -r /app/web/backend/requirements.txt

# python piro module
COPY setup.py /app/setup.py
COPY piro /app/piro
WORKDIR /app
RUN pip3 install --no-cache-dir -e .

# python backend api code
COPY web/backend/app /app/app

#### MULTI-STAGE have api serve react
FROM node as react-build

WORKDIR /app

COPY web/frontend/package.json /app/package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install


COPY web/frontend/public /app/public
COPY web/frontend/src /app/src

RUN npm run build

FROM api as api-react

COPY --from=react-build /app/build /app/web/frontend/build
ENV REACT_BUILD_DIR='web/frontend/build'
ENV ENABLE_REACT=1

#### MULTI-STAGE api-react-celery
FROM api-react as api-react-redis-celery

RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

COPY web/backend/prestart.sh /app/prestart.sh