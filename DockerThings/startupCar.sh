docker load -i allImages.tar
docker tag b884ca01feff openfaas/queue-worker:0.11.2
docker tag 4d5c7c56e1f4 openfaas/basic-auth-plugin:0.18.17
docker tag 9496eadeb6e5 openfaas/gateway:0.18.17
docker tag 8579e446340f python:2.7-alpine
docker tag 411737a82b95 nats-streaming:0.17.0
docker tag a9778f7de148 openfaas/faas-swarm:0.8.5
docker tag b97ed892eb23 prom/prometheus:v2.11.0
docker tag ce3c87f17369 prom/alertmanager:v0.18.0
docker tag 021a98fdbddd ghcr.io/openfaas/classic-watchdog:0.2.1
docker tag 3bfeb7b95ffc normchenjk/yolo-image:latest
python -m http.server --bind 0.0.0.0 8847
