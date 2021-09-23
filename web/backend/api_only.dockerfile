FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
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

