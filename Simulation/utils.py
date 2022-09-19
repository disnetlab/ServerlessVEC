from parseTraces import *
import random
from geopy.distance import geodesic

#This class supports all global Variables Required
class supportStaticVars:
    def __init__(self):
        self.ip_count=1
    def getRandomIPAddress(self):
        if self.ip_count == 12:
            self.ip_count = 13
        ip = "172.18.5."+str(self.ip_count)
        self.ip_count = self.ip_count + 1
        return ip      


#Get the Map dimensions from sumo to osm
def getDimensionsMetsAndOsm(sumoNetfile):
    print("Getting map dimensions")
    (sumoBBox, osmBBox) = getMapDimensions( sumoNetfile )
    (longLeft, latTop, longRight, latBottom) = osmBBox
    coords_1 = ( latTop, longLeft)
    coords_2 = ( latTop, longRight)
    print("hello=%s %s" %( coords_1, coords_2))
##    metersHorizontal = geodesic(coords_1, coords_2).meters
    metersHorizontal = 1000
    coords_1 = ( latTop, longLeft)
    coords_2 = ( latBottom, longLeft)
##    metersVertical = geodesic(coords_1, coords_2).meters
    metersVertical = 1000
    print(sumoBBox)
    print(type(longLeft))
    print(osmBBox)
    print((metersHorizontal, metersVertical))
    print(type(metersHorizontal))
    return(sumoBBox, osmBBox, (metersHorizontal, metersVertical))

#Translate the coordinates in sumoToPresentScreen
def translateToScreen (x, y, screenDim, sumoBBox):
    (xmin,ymin,xmax,ymax) = sumoBBox
    (screen_width, screen_height) = screenDim
##    x=xmax-x
    y=ymax-y
    return(x*screen_width/xmax, y*screen_height/ymax)

#Translate the coordinates to distance in meters
def translateInMeters(x, y, metersDim, sumoBBox):
    (xmin,ymin,xmax,ymax) = sumoBBox
    (metersHorizontal, metersVertical) = metersDim
    return(x*metersHorizontal/xmax, y*metersVertical/ymax)

#Get Random Color
def getRandColor():
    de=("%02x"%random.randint(0,255))
    re=("%02x"%random.randint(0,255))
    we=("%02x"%random.randint(0,255))
    ge="#"
    color=ge+de+re+we
    return color

#Assign Color to Cars for Visualisation
def assignColorToCars(vehicleSet):
    carColorDict={}
    for car in vehicleSet:
        carColorDict[car]=getRandColor()
    return carColorDict

#Get Random Mac Address
def getRandomMac():
    Maclist = []
    for i in range(1,4):
        RANDSTR = "".join(random.sample("0123456789abcdef",2))
        Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        
    return "00:00:00:"+RANDMAC

#Get Random IP Address
def getRandomIPAddress(supportStaticVarsObj):
    return supportStaticVarsObj.getRandomIPAddress()

#Create a circle
def create_circle(x, y, r, col, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill = col)


    
