#!/usr/bin/env bash
set -a
source app.env
set +a
docker-compose up -d --build --remove-orphans