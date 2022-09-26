import sys
from parseTraces import *
from utils import *
from tkinter import *
import time
import os

from containernet.net import Containernet
from mininet.node import RemoteController
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
from containernet.node import DockerSta
from containernet.node import Docker
from mininet.log import setLogLevel, info
from containernet.cli import CLI
from PIL import ImageTk,Image  


class Simulation:
    def __init__(self, sumoTracefile, sumoNetfile, isVisualisation, test, isMnWifi):
        print("Constructor")
        self.__isVisualisation = isVisualisation #Whether visualisation is required or not
        self.__supportStaticVars = supportStaticVars() #Support for all globals exist here
        (sumoBBox, osmBBox, metersDim)=getDimensionsMetsAndOsm(sumoNetfile)
        self.__sumoBBox = sumoBBox #Sumo Bounding Box
        self.__osmBBox = osmBBox  #OSM Bounding Box
        self.__metersDim = metersDim # HorizontalDisMeters, verticalDistMeters
        vehicleSet = getAllVehicles(sumoTracefile) #Get a set of All vehicles
        print("Num Of Vehicles=="+str(len(vehicleSet)))
        self.__vehiclePositions = parseVehicles( sumoTracefile )
        self.__carColorDict = assignColorToCars(vehicleSet)
        self.__screenDim = None #Dimensions of the screen
        self.__canvas = None #Canvas on the screen
        self.__junctions = parseJunctions( sumoNetfile )
        self.__carObjectDict = {}  #Dictionary that stores the mininet-wifi object for cars
        self.__screenObjectsDict = {} #Dictionary that stores the Tk screen object for cars
        self.__net = None #Object that stores Mininet-wifi network object
        self.__controller = None #Object that stores the Controller
        self.__win= None #Window Object
        self.__img = None #REMOVE IT LATER IF NOT REQUIRED
        self.initializeWifi() #Initialize the WiFi Object
        self.__isVisualisation = isVisualisation #Whether there should be visualisation
        self.__isMnWifi = isMnWifi
        
        if isVisualisation:
            self.initializeScreen()
        self.__junctions = parseJunctions( sumoNetfile )
        if test:
            self.simulateTraffic()

##        self.create_text(100,100, "HSHHKSKSKSJKJSJ")
##        self.__win.update_idletasks()
##        self.__win.update()
##        input()

        

    def initializeWifi(self):
        self.__net = Containernet(controller=RemoteController, link=wmediumd, wmediumd_mode=interference, ac_method='ssf')
        self.__controller = self.__net.addController('controller', controller=RemoteController, ip='192.168.56.117', port=6653 )

    def initializeScreen(self):
        self.__win= Tk()
        win = self.__win
        (xmin,ymin,xmax,ymax) = self.__sumoBBox
##        screen_width = float(win.winfo_screenwidth())
##        screen_height = float(win.winfo_screenheight())
        screen_width = 1000
        screen_height = 1000
        self.__screenDim = ( screen_width, screen_height)
        print("ScreenDim="+str(self.__screenDim))
        self.__canvas= Canvas(win,width=screen_width, height=screen_height)
        self.__canvas.pack(fill="both", expand=True)


    #This function simulates all the traffic
    def simulateTraffic(self):
        #Initialisations
        access_points = []
        kwargs = {'ssid': 'vanet-ssid', 'mode': 'n', 'passwd': '123456789a',
                  'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'kernel'}
        net = self.__net
        canvas = self.__canvas
        junctions = self.__junctions
        junctionsPosition={}
        #Add all the junctions and hosts attached to the Junctions
        for count,junctionId in enumerate(junctions.keys()):
            (posX,posY) = self.__junctions[ junctionId ]
            (metX,metY) = translateInMeters(posX, posY, self.__metersDim, self.__sumoBBox)
            randomMac = getRandomMac()
            if self.__isVisualisation:
                (scrX,scrY) = translateToScreen(posX, posY, self.__screenDim, self.__sumoBBox)
                canvas.create_rectangle(scrX, scrY, scrX+10, scrY+10,
                                    outline="#000", fill="#000")
                junctionsPosition[randomMac] = (scrX,scrY)

            pos = ','.join([str(x) for x in [metX, metY, 5]])
            apname = "ap"+str(count+1)
            ip_addr = getRandomIPAddress(self.__supportStaticVars)+"/24"
            if self.__isMnWifi:
                ap = net.addAccessPoint('ap1', ssid='new-ssid', mode='n',ip=ip_addr, channel="10", protocols='OpenFlow13', datapath='kernel',
                                 failMode="standalone", mac=randomMac, labels=['accesspoint'], 
                                 position=pos, range=1000)                
                randomMac = getRandomMac()
                attached_vm = net.addHost("D"+apname, mac=randomMac, ip = "172.18.5.12/24",cls=Docker, ports=[80,8888], mem_limit='6000m', dcmd='python -m http.server 5000' , dimage="server_example:latest")
                access_points.append((ap,attached_vm))
        #Add stations for each car
        self.addAllCars()
        if self.__isMnWifi:
            print("*** Configuring Propagation Model\n")
            net.setPropagationModel(model="logDistance", exp=2.8)
            print("*** Configuring wifi nodes\n")
            net.configureWifiNodes()
            
            #Add connection between RSUs
            numAPs = len(access_points)
            for i in range(numAPs-1):
                for j in range(i+1, numAPs):
                    print(str(i)+"----"+str(j))
                    net.addLink(access_points[i][0], access_points[j][0])
            #Add conection between AccessPoint and Docker Host for Computation
            for aps in access_points:
                ap = aps[0]
                vm = aps[1]
                net.addLink(ap,vm)
            info("*** Starting network\n")
            self.__controller.start()
            net.build()
            for aps in access_points:
                aps[0].start([self.__controller])
            net.start()
            attached_vm.cmd('./start_cluster.sh')
##            input()
            if self.__isVisualisation:
                self.__win.update_idletasks()
                self.__win.update()

##        time.sleep(200)
        self.moveVehicles(junctionsPosition)
##        info("*** Running CLI\n")
        CLI(net)
        info("*** Stopping network\n")
        net.stop()

    
    #Add stations for each cars
    def addAllCars(self):
        print("Enter Add All Cars")
        kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'kernel'}
        vehiclePositions = self.__vehiclePositions
        screenObjectsDict = self.__screenObjectsDict
        carObjectDict = self.__carObjectDict
        for vehicleDict in vehiclePositions:
            for vehicleId in [x for x in vehicleDict.keys() if x not in carObjectDict.keys()]:
                randomMac = getRandomMac()
                ip_addr = getRandomIPAddress(self.__supportStaticVars)+"/24"
                if self.__isMnWifi:
                    car = self.__net.addStation("c"+vehicleId,mac=randomMac, mode='n', ip=ip_addr, cls=DockerSta, ports=[80,8888], mem_limit='1024m', dcmd='./start_vehicle.sh', dimage="vehicle_example:latest", 
                       position='0,0,0')
                    car.cmd("""ip link set txqueuelen 100 dev `hostname`-wlan0""")
                    self.__carObjectDict[vehicleId] = car
                if self.__isVisualisation:
                    col = self.__carColorDict[ vehicleId ]
                    cir = create_circle(0, 0, 5, col, self.__canvas)
                    screenObjectsDict[ vehicleId ] = cir

    #This function iterates over timestep is sumoTrace for vehicle movement
    def moveVehicles(self, junctionsPosition):
        count=0
        win = self.__win
        connLines=[]
        podScrObj=[]
        podCmdScrObj = ""
        canvas = self.__canvas
        fp = open('numPods', 'w')
        for timestep in range(len(self.__vehiclePositions)):
            count=count+1
##            if count > 10:
##                input()
            time.sleep(1)
            podNodes = self.getPodNodes()
            numPods = sum([podNodes[x] for x in podNodes.keys()])
            fp.write(str(timestep)+","+str(numPods)+"\n")
            if self.__isVisualisation:
                if podCmdScrObj in canvas.find_all():
                    canvas.delete(podCmdScrObj)
##                podCmdScrObj=self.create_text(800, 800, podCmd)
                podCmdScrObj = canvas.create_text((800,800),fill="darkblue",font="Times 8",
                        text=str(podNodes))
                for line in connLines:
                    canvas.delete(line)
                for nums in podScrObj:
                    canvas.delete(nums)
                connLines=[]
                podScrObj=[]
                
            self.simulateTrafficHelp(timestep, junctionsPosition, connLines, podScrObj)
            if self.__isVisualisation:
                win.update_idletasks()
                win.update()
        fp.close()

    def simulateTrafficHelp(self, timestep, junctionsPosition, connLines, podScrObj):
        screenObjectsDict = self.__screenObjectsDict
        vehiclePositions = self.__vehiclePositions
        carObjectDict = self.__carObjectDict
        net = self.__net
        canvas = self.__canvas
        win = self.__win
        curTimestep = vehiclePositions [ timestep ]
        podNodes = self.getPodNodes()
        print("podNodes=%s" %podNodes)
        if "Dap1" in podNodes:
            print("Pod found on Dap1")
            junctionPos = junctionsPosition[list(junctionsPosition.keys())[0]]
            num = podNodes['Dap1']
            podNum = self.create_text(junctionPos[0], junctionPos[1], num)
            podScrObj.append(podNum)
        if(timestep == 0):
            prevTimestep = {}
        else:
            prevTimestep = vehiclePositions [ timestep-1 ]
        #Delete vehicle , move to 0,0,0,
        for vehicleId in [x for x in prevTimestep.keys() if x not in curTimestep.keys()]:
            print("Move %s to 000" %(vehicleId))
            if self.__isMnWifi:
                mininetCar = carObjectDict[ vehicleId ]
                mininetCar.setPosition('0,0,0')
            if self.__isVisualisation:
                canvas.delete(self.__screenObjectsDict[ vehicleId ])
            if self.__isMnWifi:
                c="c"+str(vehicleId)
                car = net.get(c)
                print(car.cmd("./ConnectToCluster.sh 0,0,0 stop"+" &"))
        #Remove all previous car objects
        kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
                  'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}
        print("==================Time Start======================== ")
        for vehicleId in curTimestep.keys():
            print("Vehicle="+str(vehicleId))
            posX = float(curTimestep[vehicleId][0])
            posY = float(curTimestep[vehicleId][1])
            (metX, metY) = translateInMeters (posX, posY, self.__metersDim, self.__sumoBBox)
            pos = ','.join([str(x) for x in [metX, metY, 0]])
            print("Move==="+vehicleId+"=="+pos)
            connectedMac=""

            if self.__isMnWifi:
                car = carObjectDict[ vehicleId ]
                car.setPosition(pos)
                print("---------------"+vehicleId+"-------------")
                c="c"+str(vehicleId)
                c1 = net.get(c)
                print(c1.cmd("./ConnectToCluster.sh "+str(pos)+" "+str(timestep)+" &"))
                connectedMac = self.getConnectionState(car, vehicleId, connLines)
            if self.__isVisualisation:
                ( screen_width, screen_height)  = self.__screenDim
                (scrX, scrY) = translateToScreen (posX, posY, self.__screenDim, self.__sumoBBox)
                if(screenObjectsDict[ vehicleId ] != None):
                    canvas.delete(screenObjectsDict[ vehicleId ])
                col = self.__carColorDict[ vehicleId ]
                cir = create_circle(scrX, scrY, 5, col, canvas)
                screenObjectsDict[ vehicleId ] = cir
                #Add indicator of pods on GUI
                if c in podNodes:
                    print("Pod found on %s" %c)
                    num = podNodes[c]
                    podNum = self.create_text(scrX, scrY, num)
                    podScrObj.append(podNum)
                #Check if Car is connected with RSU
                if connectedMac != "":
                    (jpX,jpY) = junctionsPosition[connectedMac]
                    print("Create line = %d %d %d %d" %(scrX, scrY, jpX, jpY))
                    line=canvas.create_line(scrX, scrY, jpX, jpY)
                    connLines.append(line)
        print("==================Time End======================== ")
                    
                    
    #This function returns the Mac address of the RSU AP, car is connected with     
    def getConnectionState(self, car, vehicleId, connLines):
        conncmd=car.cmd("iw dev c"+vehicleId+"-wlan0 link")
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        connList = re.findall(p, conncmd)
        if len(connList)>0:
            print("ConnectedTo="+str(connList))
            return connList[0]
        else:
            return ""


    def getPodNodes(self):
        apObj = self.__net.get("Dap1")
        conncmd=apObj.cmd("""docker service ps -f "desired-state=running" hello-python| awk  '$6=="Running"'| awk '{print $4}'""")
        nodeList = {}
        for node in conncmd.splitlines():
            node = node.strip()
            if node not in nodeList.keys():
                nodeList[node] = 1
            else:
                nodeList[node] = nodeList[node] +1

        return nodeList

    def create_text(self, x,y, str):
        canvas = self.__canvas
        obj=canvas.create_text((x,y-5),fill="darkblue",font="Times 15 italic bold",
                        text=str)
        return obj
        
            
        
if __name__ == "__main__":
    setLogLevel('info')
    #os.system('./deleteDockers.sh')
    # Get the parameters
    sumoTracefile = sys.argv[1]
    sumoNetfile = sys.argv[2]
    test = sys.argv[3]

    (sumoBBox, osmBBox, metersDim)=getDimensionsMetsAndOsm(sumoNetfile)

    #Start the simulation
    sim=Simulation(sumoTracefile, sumoNetfile, True,test=='1', True)


    
