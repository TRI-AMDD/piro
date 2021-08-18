# Piro web app backend API

Built using [FastAPI](https://fastapi.tiangolo.com)

## Environment variables

See [example dotenv file](.env-template) for environment variables that can be set.

You can create a web/backend/.env file or export the environment variables in the shell.
See the docker commands below for how to pass them to the docker CLI.

**MAPI_KEY** for the MaterialsProject API is required

## Run with docker

From the root of the piro repository.

### Build the image
```
docker build -t piro_backend -f web/backend/full.dockerfile .
```
Note: If "npm run build" fails due to out of memory, you can increase Docker memory resources in Docker preferences.

### Run the image
 
 ```
 # pick one of the environment variable setting methods in the below command
docker run -d --name piro_backend -p 8080:8080 -p 5555:5555 -e MAPI_KEY piro_backend  # if MAPI_KEY is already in environment
docker run -d --name piro_backend -p 8080:8080 -p 5555:5555 -e MAPI_KEY={key} piro_backend  # set MAPI_KEY manually
docker run -d --name piro_backend -p 8080:8080 -p 5555:5555 --env-file=web/backend/.env piro_backend  # use dotenv file
 ```

### Use the web app

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/api/docs>

Monitor celery workers with flower <http://0.0.0.0:5555/>


## Run for local development

### Build/Update React front end
Can skip if you only want to use the API

Requires npm binary

```
cd web/frontend
npm install
npm run build
```

Should have a web/frontend/build directory

### Setup a virtual environment
From the root of the piro repository

```
# create virtual environemnt (>= python3.7)
python3 -m venv venv

# activate it
source ./venv/bin/activate

# upgrade pip
pip install --upgrade pip

# install required 3rd party modules
pip install -r web/backend/requirements.txt

# install piro in editable mode
pip install -e .
```

### Run the app 
```
# set environment variables if not already done previously 
# export MAPI_KEY={key}

PYTHONPATH=web/backend python web/backend/app/main.py
```

### Run the celery worker

#### Using redis as the broker and backend, need a redis db running
```
docker run -d -p 6379:6379 redis
```

#### Run the worker
```
PYTHONPATH=web/backend celery -A app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 worker -l info -c 4 -Ofair --without-gossip --without-mingle
```

#### (optional) Run flower celery monitoring
```
PYTHONPATH=web/backend celery -A app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 flower 
```

### Use the web app

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/api/docs>

Monitor celery workers with flower <http://0.0.0.0:5555/>