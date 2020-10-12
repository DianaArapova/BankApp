#!/bin/sh

docker-compose -f ./docker-compose.test.yml up --build -d db-test
docker-compose -f ./docker-compose.test.yml up --build test
docker-compose -f ./docker-compose.test.yml down
