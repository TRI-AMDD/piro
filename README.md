# *piro:* rational planning of solid-state synthesis routes for inorganics
![Testing - main](https://github.com/TRI-AMDD/piro/workflows/Testing%20-%20main/badge.svg)
![Linting](https://github.com/TRI-AMDD/piro/workflows/Linting/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/TRI-AMDD/piro/badge.svg?branch=test)](https://coveralls.io/github/TRI-AMDD/piro?branch=test)

_piro_ is a recommendation system for navigation and planning of synthesis of
inorganic materials based on classical nucleation theory
and semi-empirical, data-driven approximations to its parts. Currently it
works with Materials Project data via its Rester API.

- _piro_ creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic conditions and a precursor library, 
where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics: nucleation barrier and phase-selection.

- _piro_ allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree.
(i.e. laying out the reaction pathways necessary to arrive at the target from practical/purchasable reagents/starting materials)

- _piro_ supports generation of interactive plots and a web-UI for easy-navigation.

Tutorial jupyter notebooks showing how to use _piro_ locally are provided in the [notebooks](piro/notebooks) folder.

## Prerequisites

### Python 3.7
 - `piro` uses Python 3.7.  If you wish to develop or run a local server, we recommend following the Docker instructions below to create your own `piro` container instead of configuring your local environment.

### Pymatgen API key
 - `piro` has a dependency on `pymatgen` which requires you to generate an API key.  Go [here](https://materialsproject.org/open) and follow the instructions to generate your API key.
 - Use the API key by either
    - A) adding the environment variable MAPI_KEY to your current environment
    ```
    # for example in the terminal
    export MAPI_KEY=<your API key>
    ```  
    - B) using pymatgen's command line to set a global key (note: it's PMG_MAPI_KEY instead of just MAPI_KEY)
    ```
    pmg config --add PMG_MAPI_KEY <your API key>
    ```

### Access to MongoDB Cached Database (optional)
 - Once you get the credential, set up the environment variable as follow:
      ```
      MONGODB_URI = mongodb://{username}:{password}@{host}:{port}/{database}
      ```
 - If you use conda for your development, you can do like this:
      ```
      conda env config vars set MONGODB_URI="mongodb://{username}:{password}@{host}:{port}/{database}"
      ```
 - You will need to reactive the conda environment so the change will take effective.

## Setup
There are a few options to install and run `piro` on your machine:

###  A) Get `piro` from PyPI
The most recent stable version of `piro` can be installed from [PyPI](https://pypi.org/project/piro/). We recommend installing `piro` in a dedicated environment to avoid any version conflicts for its dependencies.
```
pip install piro
```

###  B) For development, install the source from this repo in development mode
```
python setup.py develop
```


## Piro Module Usage
 - Try out a Jupyter notebook:
    ```
    jupyter notebook
    ```
   See the notebooks in piro/notebooks

## Web app

[README](web/README.md)

## Citation
If you use `piro`, we kindly ask you to cite the following publication:
* Aykol, M., Montoya, J.H., Hummelshøj, J. "Rational Solid-State Synthesis Routes for Inorganic Materials" J. Am. Chem. Soc. (2021): [https://doi.org/10.1021/jacs.1c04888](https://doi.org/10.1021/jacs.1c04888)
