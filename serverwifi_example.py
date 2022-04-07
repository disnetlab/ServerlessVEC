#!/usr/bin/python

'Setting position of the nodes'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Node, Host, OVSSwitch, Controller
from mn_wifi.node import UserAP

def topology(args):

    net = Mininet_wifi(controller=Controller,accessPoint=OVSAP)
    c1 = net.addController('c1')

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',ip='10.0.0.4', datapath='user',
                             failMode="standalone", mac='00:00:00:00:00:01',
                             position='50,50,0')
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='51,50,0')
    net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                   position='49,50,0')
    h1 = net.addHost('h1', ip='10.0.0.3/8')

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, h1)

    if '-p' not in args:
        net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    ap1.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
