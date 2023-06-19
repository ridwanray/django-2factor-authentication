# Django - DRF 2factor Authentication using an Authenticator App
This app shows .............


## Tools & Services:
- Django & DRF : for building the APIs
- Docker & Docker compose: Containerization
- PostgreSQL: Relational DB



## By the end of this tutorial 
- Onboard a user on the system
- Make a login attempt using valid credentials (email and password)
- Authenticate the user using an offline OTP generated by an Authenticator App.

## Running locally

Create a .env file by copying the .env.sample provided and run:
```
docker compose build && docker compose up
```
to start the container. As an alternative, run:
```
docker-compose -f docker-compose.dev.yml up --build
```
to build and run the container using the dev yaml file.
Make sure to externalize the db instance to be used. It can be in another container.

## Run tests
Run descriptive tests in the container using:
```
docker compose exec <docker_container_name> pytest -rP -vv
```

Access the docs on:

```
http://localhost:8000/api/v1/doc
```


# 
![Screenshot](screenshot3.png)