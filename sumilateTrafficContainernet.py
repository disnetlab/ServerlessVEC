#Import the library
from tkinter import *
from parseTraces import *
from geopy import distance
import time
import random
import sys
import math
import threading
from mininet.log import setLogLevel, info
from containernet.cli import CLI
from containernet.net import Containernet
from mn_wifi.net import Mininet_wifi
from containernet.node import DockerSta
from containernet.node import Docker
from containernet.term import makeTerm
from containernet.link import TCLink
from mininet.node import Controller
from mn_wifi.node import OVSKernelAP


from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
import os
import pdb

os.system('./deleteDockers.sh')

ymax = 5000
xmax = 5000
metMaxX = 2000
metMaxY = 2000
screenDim = (10000, 10000)
distInMetersBox = 0

sumoNetfile = ''
ip_count = 1



def translateToScreen (x, y):
    global xmax
    global ymax
    global screenDim
    (screen_width, screen_height) = screenDim
    return(x*screen_width/xmax, y*screen_height/ymax)

def translateInMeters(x, y):
    global xmax
    global ymax
    global screenDim
    global distInMetersBox
##    print(str(x)+"**"+str(y)+"**"+str(x*distInMetersBox/xmax)+"**"+str(y*distInMetersBox/ymax))
    return(x*distInMetersBox/xmax, y*distInMetersBox/ymax)
    

def getRandColor():
    de=("%02x"%random.randint(0,255))
    re=("%02x"%random.randint(0,255))
    we=("%02x"%random.randint(0,255))
    ge="#"
    color=ge+de+re+we
    return color




def getCarColor( carId, carColorDict):
    if carId in carColorDict.keys():
        return carColorDict[carId]
    else:
        carColorDict[carId]= getRandColor()
        return carColorDict[carId]


def simulateTrafficHelp( net, timestep, vehiclePositions, carObjectDict, carColorDict,  junctions, nearestJnDict):
    global xmax
    global ymax
    global screenDim
    ( screen_width, screen_height)  = screenDim
    curTimestep = vehiclePositions [ timestep ]

    if(timestep == 0):
        prevTimestep = {}
    else:
        prevTimestep = vehiclePositions [ timestep-1 ]

    #Add a new car
##    for vehicleId in [x for x in curTimestep.keys() if x not in prevTimestep.keys()]:
##        posX = float(curTimestep[vehicleId][0])
##        posY = float(curTimestep[vehicleId][1])
##        (metX, metY) = translateInMeters (posX, posY)
##
##        pos = ','.join([str(x) for x in [metX, metY, 0]])
##        print("Add==="+vehicleId)
##        c = net.addCar(vehicleId, wlans=2, position=pos, encrypt=['wpa2', ''])
##        carObjectDict[ vehicleId ] = c


    #Delete vehicle , move to 0,0,0,
    for vehicleId in [x for x in prevTimestep.keys() if x not in curTimestep.keys()]:
        print("Move %s to 000" %(vehicleId))
        mininetCar = carObjectDict[ vehicleId ]
        mininetCar.setPosition('0,0,0')
    


    #Remove all previous car objects
##    carObjectDict.clear()
    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}

    for vehicleId in curTimestep.keys():
        posX = float(curTimestep[vehicleId][0])
        posY = float(curTimestep[vehicleId][1])
        (metX, metY) = translateInMeters (posX, posY)
        pos = ','.join([str(x) for x in [metX, metY, 0]])
        print("Move==="+vehicleId+"=="+pos)

##        print(carObjectDict[ vehicleId ])
        car = carObjectDict[ vehicleId ]
        car.setPosition(pos)
        print("---------------"+vehicleId+"-------------")
        c="c"+str(vehicleId)
        c1 = net.get(c)
##        print(c1.cmd("iw dev "+c+"-wlan0 link"))
##        print(c1.cmd("ping -c 1 10.4.4.2"))
##        print(c1.cmd("curl"))


def createNearestConnection(vehicleDict, nearestJnDict, junctions, canvas ):
    global screenDim
    nearestJnDict.clear()
    for vehicleId in vehicleDict.keys():
        posX = float(vehicleDict[vehicleId][0])
        posY = float(vehicleDict[vehicleId][1])
        junctionId = findNearestJunction(posX, posY, junctions)

        jX = junctions[junctionId][0]
        jY = junctions[junctionId][1]

        (posX,posY) = translateToScreen(posX, posY)
        (jX,jY) = translateToScreen(jX, jY)
##        line = canvas.create_line(posX,posY, jX, jY, fill="blue", width=1)
        nearestJnDict[ vehicleId ] = line
        
        

def create_circle(x, y, r, col, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill = col)

        

def findNearestJunction(posX, posY, junctions):
    nearest = sys.float_info.max
    nearestId = list(junctions.keys())[0]
    for junctionId in junctions.keys():
        jX = junctions[junctionId][0]
        jY = junctions[junctionId][1]
        dist = math.sqrt((jX-posX)**2 + (jY-posY)**2)
        if(dist < nearest):
            nearest = dist
            nearestId = junctionId

    return nearestId



##for vehicleId in [x for x in prevTimestep.keys() if x not in curTimestep.keys()]:
def addAllCars(net, vehiclePositions, carObjectDict):
    print("Enter Add Cars")
    for vehicleDict in vehiclePositions:
        for vehicleId in [x for x in vehicleDict.keys() if x not in carObjectDict.keys()]:
            car = net.addStation("c"+vehicleId, passwd='123456789a', encrypt='wpa2', position='0,0,0', s_inverval=5, l_interval=10, bgscan_module="simple")
            randomMac = getRandomMac()
            ip_addr = getRandomIPAddress()
##            attached_vm = net.addDocker("D_"+vehicleId, mac=randomMac, ip = ip_addr, dimage="client_example:latest")
            attached_vm = net.addHost("D_"+vehicleId, mac=randomMac, cls=Docker, ip = ip_addr, dimage="client_example:latest")
            net.addLink(car, attached_vm)

            randomMac = getRandomMac()
            ip_addr = getRandomIPAddress()
##            car = net.addStation(vehicleId, ip=ip_addr, mac=randomMac,
##                          cls=DockerSta, dimage="ubuntu:trusty", cpu_shares=20)
            carObjectDict[vehicleId] = car
    print("Exit")
            


def getRandomIPAddress():
##    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    global ip_count
    ip = "10.4.4."+str(ip_count)
    ip_count = ip_count + 1
    return ip



def getRandomMac():
    Maclist = []
    for i in range(1,7):
        RANDSTR = "".join(random.sample("0123456789abcdef",2))
        Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        
    return RANDMAC


def simulateTraffic( vehiclePositions, sumoNetFile ):
    global xmax
    global ymax
    global screenDim
    global distInMetersBox
    print((xmax))

    carObjectDict = {}
    carColorDict = {}
    nearestJnDict = {}

    "Create a network."
    net = Containernet(controller=Controller, link=wmediumd, wmediumd_mode=interference, accessPoint=OVSKernelAP)
    over_controller=net.addController('over_controller')

    #Get Traffic junctions
    access_points = []
    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}
    junctions = parseJunctions( sumoNetfile )


    for count,junctionId in enumerate(junctions.keys()):
        (posX,posY) = junctions[ junctionId ]
        
        (metX,metY) = translateInMeters(posX, posY)

        randomMac = getRandomMac()
        pos = ','.join([str(x) for x in [metX, metY, 5]])
        ip_addr = getRandomIPAddress()

        apname = "a"+str(count+1)
        ap = net.addAccessPoint(apname, mac=randomMac, ip = ip_addr, channel='11',
                                position=pos,**kwargs)

        randomMac = getRandomMac()
        ip_addr = getRandomIPAddress()
        print("Docker ip = "+ip_addr)
##        attached_vm = net.addDocker("D_"+apname, mac=randomMac, ip = ip_addr, dcmd='python -m http.server 80', dimage="server_example:latest")
##        attached_vm = net.addHost("D_"+apname, mac=randomMac, ip = ip_addr, cls=Docker, dcmd='python -m http.server 80', dimage="server_example:latest")
##        net.addLink(ap, attached_vm)
        attached_vm = net.addHost("D_"+apname, mac=randomMac, ip = ip_addr)
        access_points.append((ap,attached_vm))

        
    addAllCars(net, vehiclePositions, carObjectDict)

    print("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    print("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    #Add all the  connectivity
    numAPs = len(access_points)
    for i in range(numAPs-1):
        for j in range(i+1, numAPs):
            print(str(i)+"----"+str(j))
            net.addLink(access_points[i][0], access_points[j][0])

    for aps in access_points:
        ap = aps[0]
        vm = aps[1]
        net.addLink(ap,vm)
        
        
    

    info("*** Starting network\n")
##    net.build()
    over_controller.start()
    net.build()
    for aps in access_points:
        ap = aps[0]
        ap.start([over_controller])
    net.ping([access_points[0][0], access_points[1][0]])


##    makeTerm(access_points[0], cmd="bash -c 'ping a2'")

    
    print("Configured WiFiNodes")
    nodes = net.stations + net.aps
    print(distInMetersBox)
    dist = str(distInMetersBox)
    net.telemetry(nodes=nodes, data_type='position',
                  min_x=0, min_y=0,
                  max_x=2000, max_y=2000)


##    pdb.set_trace()

##    x = threading.Thread(target=moveVehicles, args=(net,
##                vehiclePositions, carObjectDict, carColorDict,
##                junctions, nearestJnDict,))
##    x.start()


    info("*** Running CLI\n")
    CLI(net)

##    x.join()


    info("*** Stopping network\n")
    net.stop()


    
def moveVehicles(net, vehiclePositions,
                 carObjectDict, carColorDict,
                 junctions, nearestJnDict):
    for timestep in range(len(vehiclePositions)):
        time.sleep(.1)
        simulateTrafficHelp( net, timestep, vehiclePositions,
                                            carObjectDict, carColorDict,  junctions, nearestJnDict )

##        pdb.set_trace()
##        win.update_idletasks()
##        win.update()
    


if __name__ == "__main__":
    sumoTracefile = sys.argv[1]
    print(sumoTracefile)
    sumoNetfile = sys.argv[2]
    print(sumoNetfile)
    getMapDimensions( sumoNetfile )
    
    (sumoBBox, osmBBox) = getMapDimensions( sumoNetfile )

    (longLeft, latTop, longRight, latBottom) = osmBBox
    coords_1 = ( latTop, longLeft)
    coords_2 = ( latTop, longRight)
    distInMetersBox = distance.distance(coords_1, coords_2).meters
    print( distInMetersBox)


    
    (xmin, ymin, xmax_t, ymax_t) = sumoBBox
    print(type(xmax_t))
    vehiclePositions = {}
    vehiclePositions = parseVehicles( sumoTracefile )
    print("Parsed Traces")
    xmax = float(xmax_t)
    ymax = float(ymax_t)

    print(str(xmax)+"---"+str(ymax))
    
    simulateTraffic( vehiclePositions, sumoNetfile )

    
