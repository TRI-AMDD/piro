# syntax=docker/dockerfile:1
FROM python:3.7
ARG PYMATGEN_API_KEY
ARG MONGODB_URI
ENV USERNAME dev
ENV MAPI_KEY=$PYMATGEN_API_KEY
ENV MONGODB_URI=$MONGODB_URI

RUN python3.7 -m pip install --upgrade setuptools wheel jupyter

WORKDIR /home/$USERNAME/piro/

COPY web/dash/requirements.txt web/dash/
RUN python3.7 -m pip install -r web/dash/requirements.txt

COPY . .
RUN python3.7 -m pip install -e .

ENTRYPOINT python3.7 web/dash/app.py