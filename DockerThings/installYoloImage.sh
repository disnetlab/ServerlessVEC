#!/usr/bin/env bash


service docker start
sleep 5
docker load -i /app/allImages.tar
docker tag 3bfeb7b95ffc normchenjk/yolo-image:latest
python -m http.server 5000
