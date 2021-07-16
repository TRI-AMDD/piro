FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# this image is setup to run fastapi via gunicorn
# reference for how to use the image https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
# this should be built from root of repo

RUN apt update
RUN apt upgrade -y

# for React
RUN apt install npm -y

# 1) Install 3rd party requirements first (only copy the requirements files)
## python
COPY web/backend/requirements.txt /app/web/backend/requirements.txt
RUN python3.7 -m pip install -r /app/web/backend/requirements.txt

## react
COPY web/frontend/package-lock.json /app/web/frontend/package-lock.json
WORKDIR /app/web/frontend
RUN npm install

# 2) Then copy and install source
## react
COPY web/frontend /app/web/frontend
RUN npm build
ENV REACT_BUILD_DIR='web/frontend/build'

# python piro module
COPY setup.py /app/setup.py
COPY piro /app/piro
WORKDIR /app
RUN python3.7 -m pip install -e .

# python backend api code
COPY web/backend/app /app/app

ENV PORT=8080