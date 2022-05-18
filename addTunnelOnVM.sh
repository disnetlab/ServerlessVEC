#export CTRLIP=$1

export REMOTEIP=$1

export TAPIP=$2

export TUNNELMAC=$3

sudo ovs-vsctl add-br br1 -- set bridge br1 other-config:hwaddr=$TUNNELMAC
#sudo ovs-vsctl add-br br1 

#sudo ovs-vsctl set bridge br1 protocols=OpenFlow13

#sudo ovs-vsctl set-controller br1 tcp:$CTRLIP:6653


sudo ip addr add $TAPIP/24 dev br1

sudo ip link set br1 up

sudo ovs-vsctl add-port br1 tap1 -- set Interface tap1 type=gre options:remote_ip=$REMOTEIP


