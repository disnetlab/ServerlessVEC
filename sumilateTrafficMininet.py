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
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference

ymax = 5000
xmax = 5000
metMaxX = 2000
metMaxY = 2000
screenDim = (10000, 10000)
distInMetersBox = 0

sumoNetfile = ''

def getRandomMac():
    Maclist = []
    for i in range(1,7):
        RANDSTR = "".join(random.sample("0123456789abcdef",2))
        Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        
    return RANDMAC

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
    print(str(x)+"**"+str(y)+"**"+str(x*distInMetersBox/xmax)+"**"+str(y*distInMetersBox/ymax))
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

        print(carObjectDict[ vehicleId ])
        car = carObjectDict[ vehicleId ]
        car.setPosition(pos)







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
            car = net.addCar(vehicleId, wlans=2,position='0,0,0', encrypt=['wpa2', ''])
            carObjectDict[vehicleId] = car
    print("Exit")
            
            
            

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
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)



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
##        print(randomMac)
        apname = "e"+str(count+1)
        print(apname+"---"+pos+"--"+randomMac)
        ap = net.addAccessPoint(apname, mac=randomMac, channel='11',
                                position=pos, **kwargs)
        access_points.append(ap)

    

##    addAllCars(net, vehiclePositions, carObjectDict)
##        access_points.append(ap)

##    e1 = net.addAccessPoint('ap33', mac='00:00:00:11:00:01', channel='1',
##                            position='100,20,0', **kwargs)
    print("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    print("*** Configuring wifi nodes\n")
    net.configureWifiNodes()



    
    print("Configured WiFiNodes")
    nodes = net.cars + net.aps
    print(distInMetersBox)
    dist = str(distInMetersBox)
    net.telemetry(nodes=nodes, data_type='position',
                  min_x=0, min_y=0,
                  max_x=1800, max_y=1400)
    

##    x = threading.Thread(target=moveVehicles, args=(net,
##                vehiclePositions, carObjectDict, carColorDict,
##                junctions, nearestJnDict,))
##    x.start()


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


    
def moveVehicles(net, vehiclePositions,
                 carObjectDict, carColorDict,
                 junctions, nearestJnDict):
    for timestep in range(len(vehiclePositions)):
        time.sleep(.1)
        simulateTrafficHelp( net, timestep, vehiclePositions,
                                            carObjectDict, carColorDict,  junctions, nearestJnDict )
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

    
