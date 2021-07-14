# Piro web app backend API

## Run with docker

From the root of the piro repository.

### Build the image
```
docker build -t piro_backend --build-arg PYMATGEN_API_KEY={insert key here} --build-arg MONGODB_URI={uri} -f web/backend/Dockerfile .
```

### Run the image
 
 ```
docker run -d --name piro_backend -p 8080:8080 piro_backend
 ```

### Use the API

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/docs>


## Run for local development

From the root of the piro repository

### Setup a virtual environment

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
export PYMATGEN_API_KEY={insert key here}
export MONGODB_URI={uri}
export PYTHONPATH=web/backend
python web/backend/app/main.py
```

### Use the API

Should be available at <http://0.0.0.0:8080>

Read the API docs at <http://0.0.0.0:8080/docs>