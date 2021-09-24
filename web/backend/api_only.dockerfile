FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as api
# this image is setup to run fastapi via gunicorn
# reference for how to use the image https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
# this should be built from root of repo

# setup python and node installers
RUN apt update
RUN apt upgrade -y
RUN python3.7 -m pip install --upgrade pip

# python requirements
COPY web/backend/requirements.txt /app/web/backend/requirements.txt
RUN python3.7 -m pip install -r /app/web/backend/requirements.txt

# python piro module
COPY setup.py /app/setup.py
COPY piro /app/piro
WORKDIR /app
RUN python3.7 -m pip install -e .

# python backend api code
COPY web/backend/app /app/app

################# adding things below to deploy to AWS lambda ###################################
ARG FUNCTION_DIR="/app"

FROM api as lambda-build

ARG FUNCTION_DIR

# Install aws-lambda-cpp build dependencies
RUN apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Install the function's dependencies
RUN python3.7 -m pip install mangum
RUN python3.7 -m pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

# add another stage to try to reduce file size
FROM python:3.7-slim-buster as lambda-api
WORKDIR ${FUNCTION_DIR}
COPY --from=lambda-build ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY web/backend/lambda_entry.sh /entry.sh
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.lambda.handler" ]