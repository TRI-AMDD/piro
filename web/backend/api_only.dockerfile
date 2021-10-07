FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
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

