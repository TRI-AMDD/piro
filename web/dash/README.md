# Piro web app using Plotly Dash

## Run server locally

### install python requirements

```
pip install -r web/dash/requirements.txt
pip install -e .
```

### run the app
From root directory of this repo
```
python web/dash/app.py
```
then navigate to the link output by Dash in the command line.

## Run with docker

### Using docker container
Using the `Dockerfile` will likely be the quickest way to get a local `piro` development environment up and running with little configuration necessary on your end.

 1. Build your Docker container by running the following command from within your cloned `piro` repository, being sure to substitute your own `pymatgen` API key in place of the below `{insert key here}` portion. If you want to use the cache database, pass in the `{uri}` argument as well:
     ```
     docker build -t piro:v1 --build-arg PYMATGEN_API_KEY={insert key here} --build-arg MONGODB_URI={uri} -f web/dash/Dockerfile .
     ```

 1. Once this command is finished executing, run:
     ```
     docker run -p 8888:8888 -p 8080:8080 -it piro:v1 /bin/bash
     ```
    You can now develop with `piro` in this container

### Using docker compose
 1. Build the Docker container with Docker Compose, being sure to substitute your own `pymatgen` API key in place of the below `{insert key here}` portion. If you want to use the cache database, pass in the `{uri}` argument as well:

    ```
    cd web/dash
    docker-compose build --build-arg PYMATGEN_API_KEY={insert key here} --build-arg MONGODB_URI={uri}
    ```
 1. Run the `piro` server:
    ```
    docker-compose up
    ```
    And then navigate to the link output by Dash in the command line.

### With the container
 - Try out a Jupyter notebook:
    ```
    jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
    ```
    And then go to the link output by the `jupyter` command in your local browser.  Once you navigate to an example `jupyter` notebook in `piro/notebooks/`, you can select one to then execute in the web browser.
  
- Run a local server:
  
  ```
  python3.7 web/dash/app.py
  ```
  And then navigate to the link output by Dash in the command line.

## Debugging
  - If you receive an error like
    ```
    Creating network "piro_default" with the default driver
    ERROR: could not find an available, non-overlapping IPv4 address pool among the defaults to assign to the network
    ```
    when attempting to run the Dash server, you will likely need to disable any VPNs you may have running.
