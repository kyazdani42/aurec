# Aurec - automatic camera recorder

I wrote this to check my cat at home when taking a leave.

## What

I wanted to experiment with a service based approach and i needed different languages for different speed and library requirements.
The codebase is still under development, the webapp is a simple exploratory project to manage reading http stream manually.
missing parts:
  - Implement the authentication service with either keycloack, ory or a custom written service
  - Implement the webapp (stream reader, video list, video reader)
  - Write a mobile app (if i have some time, i want to play with kotlin)
  - review docker network security

## How can i deploy it ?

This is deployed with docker-compose (see the `docker-compose.yml` for more informations on how it works)
```bash
docker compose up --build
```
