# Synthesis App

We have a web application built using React and FastAPI.

### Docker
 - If you don't have docker, you can go [here](https://docs.docker.com/get-docker/) and follow the instructions in order to install the Docker Engine.
 - Additionally, if you would simply like to host your own local server quickly, install Docker Compose [here](https://docs.docker.com/compose/install/).

## Run as multiple containers using Docker Compose

### Environment Variables

- The docker compose uses environment variables defined in backend/.env using this as an example [example dotenv file](backend/.env-template)
- The backend requires at least the MAPI_KEY to be defined.

### Run Docker Compose

```
docker-compose up
```

### Use the web app

Should be available at <http://localhost:8080>

Read the API docs at <http://localhost:8080/api/docs>

Monitor celery workers with flower <http://localhost:5555/>


## Run as single Docker Container on locally on one machine

See backend [README](backend/README.md)
  

## Old app implementation

See Dash implementation [README](dash/README.md)