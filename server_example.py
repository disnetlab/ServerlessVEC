#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.node import Controller
from mininet.log import info, setLogLevel
from containernet.cli import CLI
from containernet.link import TCLink
from containernet.net import Containernet

setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
c0 = net.addController('c0')
info('*** Adding docker containers\n')
server = net.addDocker('server', ip='10.0.0.251',
                       dimage="server_example:latest", dcmd='python -m http.server 80')
client = net.addDocker('client', ip='10.0.0.252', dimage="client_example:latest")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(server, s1)
net.addLink(s1, s2)
net.addLink(s2, client)
info('*** Starting network\n')
##c0.start()
net.start()
info('\nclient.cmd("time curl 10.0.0.251/9999"):\n')
info(client.cmd("curl 10.0.0.251") + "\n")
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
