# *piro:* rational planning of solid-state synthesis routes for inorganics

_piro_ is a recommendation system for navigation and planning of synthesis of 
inorganic materials based on classical nucleation theory 
and semi-empirical, data-driven approximations to its parts. Currently it
works with Materials Project data via its Rester API.

- _piro_ creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic conditions and precuror library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics: nucleation barrier and phase-selection. 

- _piro_ allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree.
(i.e. laying out the reaction pathways necessary to arrive at the target from practical/purchasable reagents/starting materials)

- _piro_ supports generation of interactive plots and a web-UI for easy-navigation.

## Prerequisites

### Generate a pymatgen API key
 - `piro` has a dependency on `pymatgen` which requires you to generate an API key.  Go [here](https://materialsproject.org/open) and follow the instructions to generate your API key.

### Install Docker (optional)
 - If you wish to build and use `piro` locally within a Docker container, you will need to install Docker first if you haven't already, go [here](https://docs.docker.com/get-docker/) and follow the instructions in order to install Docker.

## Building Locally

###  Docker

Using the `Dockerfile` will likely be the quickest way to get `piro` up and running with little configuration necessary on your end.

 1. Before building your Docker container, you will need to open the `Dockerfile` file and replace `insert-api-key-here` with your own generated `pymatgen` API key (see [here](#generate-a-pymatgen-api-key)).

 1. Once you have substituted your own `pymatgen` API key, you can build your Docker container by running the following command from within your cloned `piro` repository:
     ```
     docker build -t piro:v1 .
     ```

 1. Once this command is finished executing, run:
     ```
     docker run -p 8888:8888 -it piro:v1 /bin/bash
     ```

 1. You can now develop with `piro` in this container, try out a Jupyter notebook by running:
     ```
     jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
     ```

    - Go to the link output by the `jupyter` command in your local browser.  Once you navigate to an example `jupyter` notebook in `piro/notebooks/`, you can select one to then execute in the web browser.
