#!/usr/bin/env bash

service docker start
sleep 2
#docker load -i faisalyolo.tar
#rm -f faisalyolo.tar
#docker tag 78732ecd5be5 faisalyolo:latest
docker load -i reqmediator.tar
rm -f reqmediator.tar
docker tag f1bf042e2f06 reqmediator:latest
python -m http.server 5000
