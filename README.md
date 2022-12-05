# GeoApp - API

## What is?
GeoApp is a dockerized application which has been created using the next technologies: FastAPI with Postgres, Uvicorn, and Traefik.

## How to use this project?

### Configuration
For production environments, it's needed to update the domain in *docker-compose.prod.yml*, and add your email to *traefik.prod.toml*.

### Dev: Build & Deployment

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Test it out:

1. [API](http://fastapi.localhost:8008/)
2. [API - ReDoc](http://fastapi.localhost:8008/redoc)
3. [API - Documentation](http://fastapi.localhost:8008/docs)
4. [Traefic Dashboard](http://fastapi.localhost:8081/)


### Production: Build & Deploy

Build the images and run the containers:

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```

### Related Documentation

- [TestDrivenIo Example](https://testdriven.io/blog/fastapi-docker-traefik/)