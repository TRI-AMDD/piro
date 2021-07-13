# Piro web app backend API

## Run with docker

### Build the image
This should be run from the root of the repository.
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