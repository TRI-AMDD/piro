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

ARG FUNCTION_DIR="/app"

#--------------------------------------------------------------
# MULTI-STAGE have api serve react
#--------------------------------------------------------------
FROM node as react-build

WORKDIR /app

COPY web/frontend/package.json /app/package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install


COPY web/frontend/public /app/public
COPY web/frontend/src /app/src

RUN export NODE_OPTIONS=--openssl-legacy-provider && \
    npm run build

FROM api as api-react

COPY --from=react-build /app/build /app/web/frontend/build
ENV REACT_BUILD_DIR='web/frontend/build'
ENV ENABLE_REACT=1

#--------------------------------------------------------------
# MULTI-STAGE include redis/celery for full app in single image
#--------------------------------------------------------------
FROM api-react as api-react-redis-celery

RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

COPY web/backend/prestart.sh /app/prestart.sh

#--------------------------------------------------------------
# MULTI-STAGE deploying api to aws-lambda
#--------------------------------------------------------------
FROM api as lambda-build
ARG FUNCTION_DIR="/app"

# Install awslambdaric dependencies
RUN apt-get update && apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Install the function's dependencies
RUN pip3 install --no-cache-dir mangum
RUN pip3 install --no-cache-dir --target ${FUNCTION_DIR} awslambdaric

# add another stage to try to reduce file size
FROM python:3.9-slim as lambda-api
ARG FUNCTION_DIR="/app"
WORKDIR ${FUNCTION_DIR}
COPY --from=lambda-build ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY web/backend/lambda_entry.sh /entry.sh
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.lambda.handler" ]