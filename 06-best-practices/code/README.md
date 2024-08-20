```bash
docker build -t stream-model-duration:v3 .
```

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID='whatever' \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    stream-model-duration:v3
```

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID='Test123' \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    -v $(pwd)/model:/app/model \
    stream-model-duration:v3
```

```bash
aws --endpoint-url=http://localhost:4566 kinesis list-streams

aws --endpoint-url=http://localhost:4566 kinesis create-stream --stream-name <value> --shard-count <value>
```

To prepare the project, run

```bash
make setup
```
