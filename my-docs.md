# How to run Blum bot and Blum Payload Server

## Create a shared network

`docker network create blumtelegrambot_blum_network` - since I use docker compose to run BlumBot, the name of the network will be folder_name + network_name

## Start Payload server container

```
cd ./BlumPayloadGenerator
docker build -t blum-payload-server -f ./Dockerfile .
docker run -d --name BlumPayloadServer --network blumtelegrambot_blum_network -p 9876:9876 blum-payload-server
```

## Start BlumBot

```
From project root:
docker compose up
```
