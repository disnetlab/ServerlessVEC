#!/usr/bin/env bash

service docker start
sleep 2
#docker load -i faisalyolo.tar
#rm -f faisalyolo.tar
#docker tag 78732ecd5be5 faisalyolo:latest
docker load -i reqmediator.tar
sleep 1
docker tag a05444a1d6d0 reqmediator:latest
rm -f reqmediator.tar
python -m http.server 5000
