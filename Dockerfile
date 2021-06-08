# syntax=docker/dockerfile1
ARG VERSION=18.04
FROM ubuntu:$VERSION
ARG PYMATGEN_API_KEY
ENV USERNAME dev
ENV MP_API_KEY $PYMATGEN_API_KEY
WORKDIR /home/$USERNAME

COPY . ./piro/

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

# Set ip and 
RUN find . -name 'app.py' | xargs sed -i "s/app.run_server(debug=True)/app.run_server(host='0.0.0.0', port=8888, debug=True)/g"

RUN python3.7 setup.py develop
