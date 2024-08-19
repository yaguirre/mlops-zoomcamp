#!/usr/bin/env bash

cd "$(dirname "$0")"
export LOCAL_TAG=$(date +"%Y-%m-%d-%H-%M")
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
export PREDICTIONS_STREAM_NAME="ride_predictions"

docker build -t ${LOCAL_IMAGE_NAME} ..

docker compose up --build -d

sleep 5
aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name ${PREDICTIONS_STREAM_NAME} --shard-count 1

sleep 3

pipenv run python test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

pipenv run python test-kinesis.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker compose down