export INTFACE=$1

/usr/share/openvswitch/scripts/ovs-ctl start
ovs-vsctl add-br br1 
#ifconfig br1 172.18.5.11 netmask 255.255.255.0
ovs-vsctl add-port br1 $INTFACE
ifconfig $INTFACE 0
ip link set br1 up
iw dev $INTFACE disconnect
iw dev $INTFACE connect new-ssid
iw dev $INTFACE link
ovs-vsctl add-port br1 eth1
