#!/bin/fish

# Empty Logs
rm logs/*

# Run Server Container
sudo docker compose --env-file .env up --watch --build client.bms
