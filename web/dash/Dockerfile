# syntax=docker/dockerfile:1
ARG VERSION=18.04
FROM ubuntu:$VERSION
ARG PYMATGEN_API_KEY
ARG MONGODB_URI
ENV USERNAME dev
ENV MAPI_KEY=$PYMATGEN_API_KEY
ENV MONGODB_URI=$MONGODB_URI
WORKDIR /home/$USERNAME

COPY ../.. ./piro/

RUN apt-get update \
 && apt-get -y update \
 && apt-get install --no-install-recommends -y \
    software-properties-common \
    build-essential \
 && apt-get clean -qq

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update \
 && apt-get -y update \
 && apt-get install --no-install-recommends -y \
    python3.7 \
    python3.7-dev \
    python3-pip \
 && apt-get clean -qq

RUN python3.7 -m pip install --upgrade \
    setuptools \
    numpy \
    wheel

RUN python3.7 -m pip install --upgrade \
    dash \
    jupyter

WORKDIR /home/$USERNAME/piro/

RUN python3.7 setup.py develop
