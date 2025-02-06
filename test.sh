#!/bin/fish

# Empty Logs
rm logs/*

set PROJECT_DIR $PWD
# Build Server Project
cd bms-server
eval $(pdm venv activate)
pdm build

cd $PROJECT_DIR

# Run Test Suite
sudo docker compose  -f docker-compose.yml -f compose-testing.yml up --build api.bms
bat logs/*
