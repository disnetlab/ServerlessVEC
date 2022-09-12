import sys
import xml.etree.ElementTree as ET
from geopy import distance

def getMapDimensions(sumoNetfile):
    root = ET.parse(sumoNetfile).getroot()
    for location in root.findall('location'):
        attributes = location.attrib
        sumoBBox = tuple(attributes.get('convBoundary').split(','))
        osmBBox = tuple(attributes.get('origBoundary').split(','))
        sumoBBox = tuple(float(item) for item in sumoBBox)
        osmBBox = tuple(float(item) for item in osmBBox)
        return (sumoBBox, osmBBox)
    

def parseVehicles(sumoTracefile):
    vehiclePositions = []
    root = ET.parse(sumoTracefile).getroot()
    for timestep in root.findall('timestep'):
        vehiclesTimeT = {}
        for vehicle in timestep.findall('vehicle'):
            attributes = vehicle.attrib
            id = attributes.get('id')
            posX = attributes.get('x')
            posY = attributes.get('y')
            lane = attributes.get('lane')
            PositionTuple = (posX, posY, lane)
            vehiclesTimeT[id] = PositionTuple
##            print(id +"--"+posX+"--"+posY+"--"+lane)
        vehiclePositions.append( vehiclesTimeT)

    return vehiclePositions

def parseJunctions( sumoNetfile ):
    junctions = {}
    root = ET.parse(sumoNetfile).getroot()
    for junction in root.findall('junction'):
        attributes = junction.attrib
        id = attributes.get('id')
        posX = float(attributes.get('x'))
        posY = float(attributes.get('y'))
        type = attributes.get('type')
        if type in ['traffic_light','traffic_light_unregulated']:
            junctions[id]=(posX,posY)
    return junctions
        
def getAllVehicles(sumoTracefile):
    vehicleSet=set() #Set as Set that has no duplicates
    root = ET.parse(sumoTracefile).getroot()
    for timestep in root.findall('timestep'):
        for vehicle in timestep.findall('vehicle'):
            attributes = vehicle.attrib
            id = attributes.get('id')
            vehicleSet.add(id)
    return vehicleSet     

if __name__ == "__main__":
    sumoTracefile = sys.argv[1]
    print(sumoTracefile)
    sumoNetfile = sys.argv[2]
    print(sumoNetfile)
##    getMapDimensions( sumoNetfile )
    (sumoBBox, osmBBox) = getMapDimensions(sumoNetfile)
    (longLeft, latTop, longRight, latBottom) = osmBBox
    coords_1 = ( latTop, longLeft)
    coords_2 = ( latTop, longRight)
    print( distance.distance(coords_1, coords_2).meters)
    print(str(longLeft)+"--"+str(latTop)+"--"+str(longRight)+"--"+str(latBottom))

    coords_3 = ( latTop, longLeft)
    coords_4 = ( latBottom, longLeft)
    print( distance.distance(coords_1, coords_2).meters)
    
    
    
##    parseVehicles(sumoTracefile)
    
