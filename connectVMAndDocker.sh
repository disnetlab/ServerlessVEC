export REMOTEIP=$1
export BRNAME=$2
export TAPPORTNAME=$3
export DOCKERNAME=$4
sudo ovs-vsctl add-br $BRNAME
sudo ovs-docker add-port $BRNAME eth1 $DOCKERNAME
#sudo ovs-vsctl add-port $BRNAME tap0 -- set Interface tap0 type=internal
#sudo ip addr add $TAPIP/24 dev tap0
#sudo ip link set tap0 up
sudo ovs-vsctl add-port $BRNAME $TAPPORTNAME -- set Interface $TAPPORTNAME type=gre options:remote_ip=$REMOTEIP




