# Game API

## Description
Simple Django REST API for user registration, token-based authentication, and a game logic.

## Requirements
- Docker


## How to run
1. Build Docker image:
```bash
docker build -t game-api .
```
2.  Run container
```bash
docker run -p 8000:8000 game-api
```
You can build and run the Docker container in a single command using &&. First, the image is built, then immediately the container is started.
```bash
docker build -t game-api . && docker run -p 8000:8000 game-api
```


## Notes

Default DB: SQLite

All configurations set to defaults for easy local testing