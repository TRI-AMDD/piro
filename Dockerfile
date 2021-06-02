# syntax=docker/dockerfile1
ARG VERSION=20.04
FROM ubuntu:$VERSION
ENV USERNAME dev
# Insert your generated `pymatgen` API key below in place of
# `insert-api-key-here` before building
ENV MP_API_KEY insert-api-key-here
WORKDIR /home/$USERNAME

COPY . ./piro/

RUN apt-get update \
 && apt-get -y update \
 && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
 && apt-get clean -qq

RUN pip3 install -U numpy Cython jupyter

RUN git clone https://github.com/hackingmaterials/matminer.git

WORKDIR /home/$USERNAME/matminer/

# A pinned version of `matminer` with most recent `pymatgen` import patches
RUN git checkout dd6a7326dca0f28527c76a0a5a6b9198999fb558

RUN python3 setup.py install

WORKDIR /home/$USERNAME/piro/

RUN python3 setup.py develop
