# *piro:* rational planning of solid-state synthesis routes for inorganics
![Testing - main](https://github.com/TRI-AMDD/piro/workflows/Testing%20-%20main/badge.svg)
![Linting](https://github.com/TRI-AMDD/piro/workflows/Linting/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/TRI-AMDD/piro/badge.svg?branch=test)](https://coveralls.io/github/TRI-AMDD/piro?branch=test)

_piro_ is a recommendation system for navigation and planning of synthesis of
inorganic materials based on classical nucleation theory
and semi-empirical, data-driven approximations to its parts. Currently it
works with Materials Project data via its Rester API.

- _piro_ creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic conditions and precuror library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics: nucleation barrier and phase-selection.

- _piro_ allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree.
(i.e. laying out the reaction pathways necessary to arrive at the target from practical/purchasable reagents/starting materials)

- _piro_ supports generation of interactive plots and a web-UI for easy-navigation.

## Prerequisites

### Python 3.7
 - `piro` uses Python 3.7.  If you wish to develop or run a local server, we recommend following the Docker instructions below to create your own `piro` container instead of configuring your local environment.

### Pymatgen API key
 - `piro` has a dependency on `pymatgen` which requires you to generate an API key.  Go [here](https://materialsproject.org/open) and follow the instructions to generate your API key.

### Access to MongoDB Cached Database
 - Once you get the credential, set up the environment variable as follow:
      ```
      MONGODB_URI = mongodb://{username}:{password}@{host}:{port}/{database}
      ```
 - If you use conda for your development, you can do like this:
      ```
      conda env config vars set MONGODB_URI="mongodb://{username}:{password}@{host}:{port}/{database}"
      ```
 - You will need to reactive the conda environment so the change will take effective.


### Docker (optional)
 - If you wish to develop on and build `piro`, the easiest way to get started is Docker. If you haven't already, go [here](https://docs.docker.com/get-docker/) and follow the instructions in order to install the Docker Engine.
 - Additionally, if you would simply like to host your own local server quickly, install Docker Compose [here](https://docs.docker.com/compose/install/).

## Setup

###  - `piro` Environment for Local Development

Using the `Dockerfile` will likely be the quickest way to get a local `piro` development environment up and running with little configuration necessary on your end.

 1. Build your Docker container by running the following command from within your cloned `piro` repository, being sure to substitute your own `pymatgen` API key in place of the below `{insert key here}` portion. If you want to use the cache database, pass in the `{uri}` argument as well:
     ```
     docker build -t piro:v1 --build-arg PYMATGEN_API_KEY={insert key here} --build-arg MONGODB_URI={uri}.
     ```

 1. Once this command is finished executing, run:
     ```
     docker run -p 8888:8888 -p 8080:8080 -it piro:v1 /bin/bash
     ```
    You can now develop with `piro` in this container

### - `piro` Local Server Hosting
 1. Build the Docker container with Docker Compose, being sure to substitute your own `pymatgen` API key in place of the below `{insert key here}` portion. If you want to use the cache database, pass in the `{uri}` argument as well:

    ```
    docker-compose build --build-arg PYMATGEN_API_KEY={insert key here} --build-arg MONGODB_URI={uri}
    ```
 1. Run the `piro` server:
    ```
    docker-compose up
    ```
    And then navigate to the link output by Dash in the command line.

## Usage

 - Rebuild the codebase:
   - Natively:
     ```
     python setup.py develop
     ```
   - In Docker:
     ```
     python3.7 setup.py develop
     ```
 - Try out a Jupyter notebook:
   - Natively:
     ```
     jupyter notebook
     ```
   - In Docker:
     ```
     jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
     ```
     And then go to the link output by the `jupyter` command in your local browser.  Once you navigate to an example `jupyter` notebook in `piro/notebooks/`, you can select one to then execute in the web browser.
  - Run a local server:
    - Natively:
      ```
      python web/app.py
      ```
    - In Docker:
      ```
      python3.7 web/app.py
      ```
      And then navigate to the link output by Dash in the command line.

## Debugging
  - If you receive an error like
    ```
    Creating network "piro_default" with the default driver
    ERROR: could not find an available, non-overlapping IPv4 address pool among the defaults to assign to the network
    ```
    when attempting to run the Dash server, you will likely need to disable any VPNs you may have running.

## Citation
If you use `piro`, we kindly ask you to cite the following publication:
* Aykol, M., Montoya, J.H., Hummelshøj, J. "Rational Solid-State Synthesis Routes for Inorganic Materials" J. Am. Chem. Soc. (2021): [https://doi.org/10.1021/jacs.1c04888](https://doi.org/10.1021/jacs.1c04888)
