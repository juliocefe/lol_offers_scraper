#!/bin/bash
# supposing docker-compose does not exists! :D
# I did this because I am trying to learn more about how docker works
echo "Creating our network..."
docker network create --attachable lol_offers

echo "Running selenium container..."
docker run --rm -dp 4444:4444 --name selenium selenium/standalone-chrome
echo "Sleeping 8 seconds so the selenium container begins..."
sleep 8s

echo "Attaching selenium container to our network..."
docker network connect lol_offers selenium 

echo "Runnning our python container program..."
docker run --rm --network lol_offers --env-file ./secrets.txt app

echo "Stopping selenium container..."
docker rm -f selenium

echo "Removing network..."
docker network rm lol_offers