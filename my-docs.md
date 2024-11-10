# How to run Blum bot and Blum Payload Server

## Create a shared network

`docker network create blum_network`

## Start Payload server container

```
cd ./BlumPayloadGenerator
docker build -t blum-payload-server -f ./Dockerfile .
docker run -d --name BlumPayloadServer --network blum_network -p 9876:9876 blum-payload-server
```

## Start BlumBot

```
From project root:
docker compose up
```
