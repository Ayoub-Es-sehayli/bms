#!/bin/fish

set PROJECT_DIR $PWD
# Build Server Project
cd bms-server
eval $(pdm venv activate)
pdm build

cd $PROJECT_DIR

# Run Server Container
sudo docker compose --env-file .env up -d --build api.bms
sudo docker compose logs -f api.bms
