interface="$1"
ip_addr=$(ip addr show $interface | awk '$1 == "inet" {gsub(/\/.*$/, "", $2); print $2}')
service docker start

sleep 1

docker swarm init --advertise-addr "$ip_addr" --default-addr-pool 173.19.0.0/16 | tee joinLink
cd faas-0.18.18
./deploy_stack.sh --no-auth

