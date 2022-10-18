#!/usr/bin/env bash

interface="`hostname`-eth0"
ip_addr=$(ip addr show $interface | awk '$1 == "inet" {gsub(/\/.*$/, "", $2); print $2}')
service docker start
echo "$ip_addr"
sleep 2

for image in "/app/OpenFaasImages"/*
do
        echo ${image}
#        docker load -i $image
done


#cd Images
#docker import alertmanager.tar prom/alertmanager
#docker import basicauth.tar openfaas/basic-auth-plugin
#docker import faasswarm.tar openfaas/faas-swarm
#docker import gateway.tar openfaas/gateway
#docker import natsstreaming.tar nats-streaming
#docker import normchenjk.tar normchenjk/yolo-image
#docker import prometheus.tar prom/prometheus
#docker import queueworker.tar openfaas/queue-worker
#cd ..

docker load -i allImages.tar
#docker load -i faisalyolo.tar
docker load -i reqmediator.tar

docker tag b884ca01feff openfaas/queue-worker:0.11.2
docker tag 4d5c7c56e1f4 openfaas/basic-auth-plugin:0.18.17
docker tag 9496eadeb6e5 openfaas/gateway:0.18.17
docker tag 8579e446340f python:2.7-alpine
docker tag 411737a82b95 nats-streaming:0.17.0
docker tag a9778f7de148 openfaas/faas-swarm:0.8.5
docker tag b97ed892eb23 prom/prometheus:v2.11.0
docker tag ce3c87f17369 prom/alertmanager:v0.18.0
docker tag 021a98fdbddd ghcr.io/openfaas/classic-watchdog:0.2.1

docker tag f1bf042e2f06 reqmediator:latest
#Remove faisalyolo
docker rmi 78732ecd5be5

#rm -f faisalyolo.tar
rm -f reqmediator.tar
rm -f allImages.tar
docker swarm init --advertise-addr "$ip_addr" --default-addr-pool 173.19.0.0/16 | tee joinLink
cd faas-0.18.18
./deploy_stack.sh --no-auth
#docker tag 3bfeb7b95ffc normchenjk/yolo-image:latest
#docker rmi normchenjk/yolo-image:latest
docker tag f1bf042e2f06 reqmediator:latest
#docker tag 78732ecd5be5 faisalyolo:latest


cd /app
#docker tag 78732ecd5be5 faisalyolo:latest
docker tag f1bf042e2f06 reqmediator:latest
./faas-cli build -f /app/hello-python.yml

sleep 3
#docker tag 78732ecd5be5 faisalyolo:latest
docker tag f1bf042e2f06 reqmediator:latest
./faas-cli deploy -f hello-python.yml


#docker node update --label-add accesspoint Dap1
#docker service update --placement-pref-add spread=node.labels.accesspoint hello-python
#docker service update --force --update-order start-first hello-python
docker service update --force --update-order start-first --health-interval 1s --health-retries 2 --health-start-period 80s --health-timeout 1s --update-parallelism 1 --update-delay 1s --update-monitor 90s --rollback-order start-first hello-python

./removeNodes.sh 2>/dev/null 1>/dev/null &


sleep 10
curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python
echo "------------------------"
sleep 3
curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python
echo "------------------------"
sleep 3
curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python
echo "------------------------"
sleep 3
curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python
echo "------------------------"
sleep 3
curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python
echo "------------------------"
sleep 3

#python spreadCluster.py &

echo "Hello"
docker swarm join-token worker| grep join > index.html
