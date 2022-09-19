#!/usr/bin/env bash

service docker start
sleep 2
docker load -i faisalyolo.tar
rm -f faisalyolo.tar
docker tag c0b511254b58 faisalyolo:latest
python -m http.server 5000
