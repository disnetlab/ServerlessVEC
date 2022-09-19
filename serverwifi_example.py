#!/usr/bin/python

'Setting position of the nodes'
#, network="multi"
import sys
import random
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
import pdb


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
    for i in range(1,7):
        RANDSTR = "".join(random.sample("0123456789abcdef",2))
        Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        
    return RANDMAC

def topology(args):

    net = Containernet(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, ac_method='ssf')
    c1 = net.addController('c1', controller=RemoteController, ip='192.168.56.117', port=6653 )
##
    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='n',ip='172.18.5.13/24', channel="10", protocols='OpenFlow13', datapath='kernel',
                             failMode="standalone", mac='00:00:00:00:00:01',range='500',
                             position='50,50,0')
    attached_vm = net.addHost("Dap1", mac='00:00:00:00:00:12', ip = '172.18.5.12/24', cls=Docker, ports=[80,8080], mem_limit='4096m', dimage="server_example:latest")



##    ap2 = net.addAccessPoint('ap2', ssid='new-ssid', mode='b',ip='172.18.5.113/24', protocols='OpenFlow13', datapath='kernel',
##                             failMode="standalone", mac='00:00:01:00:00:01',
##                             position='150,150,0')
##    Dap2 = net.addHost("Dap2", mac='00:00:03:00:00:12', ip = '172.18.5.112/24', cls=Docker, ports=[80,8888], dcmd='python -m http.server --bind 0.0.0.0 80', dimage="server_example:latest")



    
    sta1 = net.addStation('sta1',mac='00:00:00:00:00:02', ip='172.18.5.11/24', cls=DockerSta, ports=[80,8888], mem_limit='4096m', dcmd='./installYoloImage.sh', dimage="server_example:latest", 
                   position='51,50,0')
##    pos='49,50,0'
##    d1 = net.get('sta1')
##    print(d1.cmd("./startupCar.sh"))
    
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='172.18.5.10/24', cls=DockerSta, ports=[80,8888], mem_limit='4096m', dcmd='./installYoloImage.sh', dimage="server_example:latest", 
                   position='52,50,0')
##    pos='49,50,0'
##    d1 = net.get('sta2')
##    print(d1.cmd("./startupCar.sh"))


##    stas=[]
##    for i in range(1,15):
##        ip=getRandomIPAddress()+"/24"
##        mac=getRandomMac()
##        sta = net.addStation('sta'+str(i),  mode='b',mac=mac, ip=ip, cls=DockerSta, ports=[80,8888], dcmd='python -m http.server --bind 0.0.0.0 80', dimage="server_example:latest", 
##                   position='49,50,0')
##        stas.append(sta)
        


    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    
    net.configureWifiNodes()
    net.addLink(ap1, attached_vm)
##    net.addLink(ap2, Dap2)
##    net.addLink(ap1, ap2)


    info("*** Creating links\n")


    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
##    ap2.start([c1])
    net.start()
##    ap2.start([c1])


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
