#!/usr/bin/python

'Setting position of the nodes'
#, network="multi"
import sys

from mininet.log import setLogLevel, info


from mininet.node import Node, Host, OVSSwitch, Controller, RemoteController


from mininet.log import setLogLevel, info
from containernet.cli import CLI
from containernet.net import Containernet
from mn_wifi.net import Mininet_wifi
from containernet.node import DockerSta
from containernet.node import Docker
from containernet.term import makeTerm
from containernet.link import TCLink
from mininet.node import RemoteController
from mn_wifi.node import OVSKernelAP
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
from mininet.log import setLogLevel



def topology(args):

    net = Containernet(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, accessPoint=OVSKernelAP)
    c1 = net.addController('c1', controller=RemoteController, ip='192.168.56.101', port=6653 )
##
    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='b', channel='1',ip='10.10.10.2', protocols='OpenFlow13', datapath='user',
                             failMode="standalone", mac='00:00:00:00:00:01',
                             position='50,50,0')
    attached_vm = net.addHost("Dap", mac='00:00:00:00:00:12', ip = '10.10.10.3', cls=Docker, ports=[80], dcmd='python -m http.server --bind 0.0.0.0 80', dimage="server_example:latest")

    
    sta1 = net.addStation('sta1',  mode='p',mac='00:00:00:00:00:02', ip='10.10.10.4', cls=DockerSta, ports=[80], dcmd='python -m http.server --bind 0.0.0.0 80', dimage="server_example:latest", 
                   position='51,50,0')
    
    sta2 = net.addStation('sta2', mode='p', mac='00:00:00:00:00:03', ip='10.10.10.6', cls=DockerSta, ports=[80], dcmd='python -m http.server --bind 0.0.0.0 80', dimage="server_example:latest", 
                   position='49,50,0')

    sta3 = net.addStation('sta3', mac='00:00:44:00:01:03', ip='10.10.10.9', 
                   position='49,50,0')

    sta4 = net.addStation('sta4', mac='00:00:00:35:00:03', ip='10.10.10.12', 
                   position='49,50,0')


    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.addLink(ap1, attached_vm, cls=TCLink)


    info("*** Creating links\n")


    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    net.start()
##    ap2.start([c1])


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('debug')
    topology(sys.argv)
