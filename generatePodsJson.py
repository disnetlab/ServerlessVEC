from parseTraces import *
import random
from geopy.distance import geodesic
import csv
import json


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
        vehiclePositions.append(vehiclesTimeT)
    return vehiclePositions

def parseJunctions( sumoNetfile ):
    junctions = {}
    root = ET.parse(sumoNetfile).getroot()
    count = 1
    for junction in root.findall('junction'):
        attributes = junction.attrib
        id = attributes.get('id')
        posX = float(attributes.get('x'))
        posY = float(attributes.get('y'))
        type = attributes.get('type')
        apname = "Dap"+str(count)
        count = count + 1
        if type in ['traffic_light','traffic_light_unregulated']:
            junctions[apname]={'x':posX, 'y':posY}
    return junctions


def parseDetailsFile(podsDetailsFile):
    podsDict={}
    with open(podsDetailsFile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            tempDict = {}
            pods_detail = row[1]
            timestep =row[0]
##            print(pods_detail)
            for node_pod in pods_detail.split(';'):
                node=node_pod.split(':')[0]
                pod=node_pod.split(':')[1]
##                print(node)
##                print(pod)
                tempDict[node]=pod
            podsDict[int(timestep)] = tempDict
    return podsDict

def generateJSON(vehiclePositions, podsDict):
    jsonDict = {}
    for vehicle_timestep in range(len(vehiclePositions)):
        
        vehtime = vehiclePositions[vehicle_timestep]
        podstime = podsDict[vehicle_timestep]
        timeDict = {}
        for id in vehtime.keys():
            presentDict={}
            (x,y,lane) = vehtime[id]
            car = "c"+id
            if car in podstime.keys():
                numpods = podstime[car]
            else:
                numpods=0
            presentDict['x']=x
            presentDict['y']=y
            presentDict['pod']=numpods
            timeDict[car] = presentDict
        for node in podstime.keys():
            presentDict={}
            if node.startswith('Dap'):
                numpods = podstime[node]
                presentDict['pod'] = numpods
                timeDict[node] = presentDict

        jsonDict[vehicle_timestep] = timeDict

    return jsonDict

                
            
            
            
            
##        for vehicles in vehtime.keys():
##            print(vehicles)
        
            

if __name__ == "__main__":
    sumoTracefile = sys.argv[1]
    vehiclePositions = parseVehicles(sumoTracefile)
    podsDetailsFile = sys.argv[2]
    sumoNetfile = sys.argv[3]
    podsDict = parseDetailsFile(podsDetailsFile)
    jsonDict = generateJSON(vehiclePositions, podsDict)
##    print(jsonDict)
    with open("jsonDump.json", "w") as outfile:
        json.dump(jsonDict, outfile)

    junctions = parseJunctions( sumoNetfile )
    with open("rsuDump.json", "w") as outfile:
        json.dump(junctions, outfile)


    
    
