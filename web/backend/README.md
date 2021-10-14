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
# can use --target to select stages (api|api-react|api-react-redis-celery)
docker build --target api -t piro_backend -f web/backend/Dockerfile .
```
Note: If "npm run build" fails due to out of memory, you can increase Docker memory resources in Docker preferences.

### Run the image
 
 ```
 # pick one of the environment variable setting methods in the below command
docker run -d --name piro_backend -p 80:80 -p 5555:5555 -e MAPI_KEY piro_backend  # if MAPI_KEY is already in environment
docker run -d --name piro_backend -p 80:80 -p 5555:5555 -e MAPI_KEY={key} piro_backend  # set MAPI_KEY manually
docker run -d --name piro_backend -p 80:80 -p 5555:5555 --env-file=web/backend/.env piro_backend  # use dotenv file
 ```

### Use the web app

(stage: api)
Read the API docs at <http://localhost/api/docs>

(stage: api-react)
React UI should be available at <http://localhost>

(stage: api-react-redis-celery)
Monitor celery workers with flower <http://localhost:5555/>


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

python -m web.backend.app.main
```

### Run the celery worker

#### Using redis as the broker and backend, need a redis db running
```
docker run -d -p 6379:6379 redis
```

#### Run the worker
```
celery -A web.backend.app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 worker -l info -c 4 -Ofair --without-gossip --without-mingle
```

#### (optional) Run flower celery monitoring
```
celery -A web.backend.app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 flower 
```

### Use the web app

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/api/docs>

Monitor celery workers with flower <http://0.0.0.0:5555/>

## commands to create Lambda docker image
```
# from piro repo root directory

# build and run
docker build -t synthesis-app-lambda -f web/backend/Dockerfile .
docker run -d --name synthesis-app-lambda -p 9000:8080 --env-file=web/backend/.env synthesis-app-lambda

# try it out
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @web/backend/lambda_request.json

# commit the image and push to ECR
docker commit synthesis-app-lambda
# follow ECR push instructions from AWS
# add AWS env variables, and run aws login command
# docker tag <the previously committed image> <ecr image url>
# docker push <ecr image url>
```
