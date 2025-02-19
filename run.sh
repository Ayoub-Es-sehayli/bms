#!/bin/fish

# Run Server Container
sudo docker compose \
  -f docker-compose.yml -f compose-develop.yml \
  --env-file .env up --watch --build \
  api.bms client.bms
