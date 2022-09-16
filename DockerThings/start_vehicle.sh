#!/usr/bin/env bash

service docker start
sleep 2
docker load -i normanchenImg.tar

docker tag 3bfeb7b95ffc normchenjk/yolo-image:latest
python -m http.server 5000
