#!/usr/bin/env bash

sleep 4
interface="`hostname`-eth0"
ip_addr=$(ip addr show $interface | awk '$1 == "inet" {gsub(/\/.*$/, "", $2); print $2}')
service docker start
echo "$ip_addr"
sleep 1

docker swarm init --advertise-addr "$ip_addr" --default-addr-pool 173.19.0.0/16 | tee joinLink
cd faas-0.18.18
./deploy_stack.sh --no-auth

cd /app
./faas-cli build -f /app/hello-python.yml
./faas-cli deploy -f hello-python.yml

docker swarm join-token worker| grep join > index.html
python -m http.server 5000 
