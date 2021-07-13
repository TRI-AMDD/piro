FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# this image is setup to run fastapi via gunicorn
# reference for how to use the image https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi

# copy only the requirements file and get most non-changing requirements installed
COPY ./web/backend/requirements.txt ./web/backend/requirements.txt
RUN python3.7 -m pip install -r ./web/backend/requirements.txt

# copy piro and install that locally
COPY ./setup.py setup.py
COPY ./piro piro
RUN python3.7 -m pip install -e .

# copy web app files
COPY web/backend/app ./app

# set environment variables
ARG PORT
ENV PORT=8080

ARG PYMATGEN_API_KEY
ENV MAPI_KEY=$PYMATGEN_API_KEY

ARG MONGODB_URI
ENV MONGODB_URI=$MONGODB_URI

