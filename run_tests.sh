#!/bin/sh

docker-compose -f ./docker-compose.test.yml up -d --build db
docker-compose -f ./docker-compose.test.yml up --build web
docker-compose -f ./docker-compose.test.yml down -v
