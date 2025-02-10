#!/bin/fish

# Empty Logs
rm logs/*

# Run Test Suite
sudo docker compose  -f docker-compose.yml -f compose-testing.yml up --watch --build api.bms
bat logs/pytest.log
