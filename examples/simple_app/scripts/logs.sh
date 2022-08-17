#! /bin/bash
docker compose -f docker-compose.example.yaml logs ${1:-example_flaskapp}