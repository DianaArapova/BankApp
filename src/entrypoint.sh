#!/bin/sh

echo "Waiting for postgres..."

sleep 1

echo "PostgreSQL started"

exec "$@"
