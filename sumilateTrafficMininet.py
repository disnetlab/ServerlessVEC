#!/usr/bin/env python

'Setting position of the nodes'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Node, Host, OVSSwitch, Controller, RemoteController
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
import random



ip_count=20
def getRandomIPAddress():
##    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    global ip_count
    if ip_count == 12:
        ip_count = 13
    ip = "172.18.5."+str(ip_count)
    ip_count = ip_count + 1
    return ip

def getRandomMac():
    Maclist = []
    for i in range(1,4):
        RANDSTR = "".join(random.sample("0123456789abcdef",2))
        Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        
    return "00:00:00:"+RANDMAC


def topology(args):

    net = Mininet_wifi(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, ac_method='ssf')
    c1 = net.addController('c1', controller=RemoteController, ip='192.168.56.117', port=6653 )

    info("*** Creating nodes\n")
##    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
##                             failMode="standalone", mac='00:00:00:00:00:01',
##                             position='50,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='b',ip='172.18.5.1/24', protocols='OpenFlow13', datapath='kernel',
                         failMode="standalone", mac='00:00:00:00:00:01',
                         position='50,50,0')
##    net.addStation('sta1', mac='00:00:00:00:00:02', ip='172.18.5.18/24',
##                   position='30,60,0')
##    net.addStation('sta2', mac='00:00:00:00:00:03', ip='172.18.5.19/24',
##                   position='70,30,0')
    stas=[]
    for i in range(1,15):
        ip=getRandomIPAddress()+"/24"
        mac=getRandomMac()
        pos='50,'+str(50+i)+',0'
        sta = net.addStation('sta'+str(i),  mode='b',mac=mac, ip=ip, 
                   position=pos)
        stas.append(sta)
    h1 = net.addHost('h1', ip='10.0.0.3/8')

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
##    net.addLink(ap1, h1)

    if '-p' not in args:
        net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    net.start()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('debug')
    topology(sys.argv)
