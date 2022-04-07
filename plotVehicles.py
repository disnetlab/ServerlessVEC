#Import the library
from tkinter import *
from parseTraces import *
from geopy import distance
import time
import random
import sys
import math
import pdb

ymax = 5000
xmax = 5000
screenDim = (10000, 10000)
distInMetersBox = 0

sumoNetfile = ''

def translateToScreen (x, y):
    global xmax
    global ymax
    global screenDim
    (screen_width, screen_height) = screenDim
    return(x*screen_width/xmax, y*screen_height/ymax)

def translateinMeters(x, y):
    global xmax
    global ymax
    global screenDim
    print(float(x*distInMetersBox/xmax)+"--"+float(y*distInMetersBox/ymax))
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


def simulateTrafficHelp( timestep, vehiclePositions, carObjectDict, carColorDict, canvas, junctions, nearestJnDict):
    global xmax
    global ymax
    global screenDim

    ( screen_width, screen_height)  = screenDim

    curTimestep = vehiclePositions [ timestep ]
    
##    print("keys="+str(list(lastTstep.keys())))
    for carId in carObjectDict.keys():
        canvas.delete(carObjectDict[ carId ])
##        print("deleting carId "+carId)

    #Remove all previous car objects
    carObjectDict.clear()
    
    for vehicleId in curTimestep.keys():
        locX = float(curTimestep[vehicleId][0])
        locY = float(curTimestep[vehicleId][1])
        (locX, locY) = translateToScreen (locX, locY)
##        print("Creating %s circle at %s %s " %(vehicleId, locX, locY))
        col = getCarColor( vehicleId, carColorDict)
        cir = create_circle(locX, locY, 5, col, canvas)
        carObjectDict[ vehicleId ] = cir

    createNearestConnection(curTimestep, nearestJnDict, junctions, canvas )




def createNearestConnection(vehicleDict, nearestJnDict, junctions, canvas ):
    global screenDim

    for vehicleId in nearestJnDict.keys():
        canvas.delete(nearestJnDict[vehicleId])

    nearestJnDict.clear()

    for vehicleId in vehicleDict.keys():
        posX = float(vehicleDict[vehicleId][0])
        posY = float(vehicleDict[vehicleId][1])
        junctionId = findNearestJunction(posX, posY, junctions)

        jX = junctions[junctionId][0]
        jY = junctions[junctionId][1]

        (posX,posY) = translateToScreen(posX, posY)
        (jX,jY) = translateToScreen(jX, jY)
        line = canvas.create_line(posX,posY, jX, jY, fill="blue", width=1)
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
        
    

def simulateTraffic( vehiclePositions, sumoNetFile ):
    global xmax
    global ymax
    global screenDim
    global distInMeters
    print((xmax))

    carObjectDict = {}
    carColorDict = {}
    nearestJnDict = {}

    
    win= Tk()
    screen_width = float(win.winfo_screenwidth())
    screen_height = float(win.winfo_screenheight())
    screenDim = ( screen_width, screen_height)
    canvas= Canvas(win,width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    
    #Print the screen size
##    print("Screen width:", screen_width)
##    print("Screen height:", screen_height)

    #Get Traffic junctions
    junctions = parseJunctions( sumoNetfile )
    for junctionId in junctions.keys():
        (posX,posY) = junctions[ junctionId ]
        (posX,posY) = translateToScreen(posX, posY)
        canvas.create_rectangle(posX, posY, posX+5, posY+5,
                                outline="#000", fill="#000")


    for timestep in range(len(vehiclePositions)):
        time.sleep(.1)
        simulateTrafficHelp( timestep, vehiclePositions,
                                            carObjectDict, carColorDict, canvas,  junctions, nearestJnDict )
        win.update_idletasks()
        win.update()
##        break
    win.mainloop()

    

    


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

    
