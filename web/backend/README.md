# Piro web app backend API

Built using [FastAPI](https://fastapi.tiangolo.com)

## Environment variables

See [settings code](app/settings.py) or [example dotenv file](.env-template) for environment variables that can be set.

You can create a web/backend/.env file or export the environment variables in the shell

**MAPI_KEY** for the MaterialsProject API is required

## Run with docker

From the root of the piro repository.

### Build the image
```
docker build -t piro_backend -f web/backend/Dockerfile .
```
Note: If "npm run build" fails due to out of memory, you can increase Docker memory resources in Docker preferences.

### Run the image
 
 ```
 # pick one of the environment variable setting methods in the below command
docker run -d --name piro_backend -p 8080:8080 -e MAPI_KEY piro_backend  # if MAPI_KEY is already in environment
docker run -d --name piro_backend -p 8080:8080 -e MAPI_KEY={key} piro_backend  # set MAPI_KEY manually
docker run -d --name piro_backend -p 8080:8080 --env-file=web/backend/.env piro_backend  # use dotenv file

 ```

### Use the API

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/docs>


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
# set environment variables if not already done previously or in a web/backend/.env 
# export MAPI_KEY={key}

PYTHONPATH=web/backend python web/backend/app/main.py
```

### Use the API

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/docs>