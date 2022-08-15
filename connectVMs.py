import paramiko
import os
import subprocess
import csv
import netifaces as ni

presentTapPortNum=0
presentBridgeNum=0
presentVMNumber=0
VMDict=list()
VMAssociations={}
LocalPswd="wifi"

def getIPAddress():
    ip = ni.ifaddresses('enp0s9')[ni.AF_INET][0]['addr']
    return ip
def getDockerName(stationName):
    dockerName="mn."+stationName
    return dockerName

def getNewTapPortName():
    global presentTapPortNum
    tapPortName="tap"+str(presentTapPortNum)
    presentTapPortNum=presentTapPortNum+1
    return tapPortName

def getNewBridgeName():
    global presentBridgeNum
    bridgeName="br"+str(presentBridgeNum)
    presentBridgeNum=presentBridgeNum+1
    return bridgeName

def readVMFile():
    global VMDict
    with open('VMsAvailable.csv') as csv_file:
        VMDict = list(csv.reader(csv_file, delimiter=','))

def getNewVM():
    global presentVMNumber
    global VMDict
    print(type(VMDict))
    print("Len="+str(len(VMDict)))
    vm=VMDict[presentVMNumber]
    presentVMNumber=presentVMNumber+1
    return vm

def getResourcesUsedForVM(entityName,staOrAP):
    ResourcesDict={}
    if staOrAP:
        ResourcesDict['TYPE']="STATION"
        ResourcesDict['BRNAME']=getNewBridgeName()
        ResourcesDict['TAPNAME']=getNewTapPortName()
        ResourcesDict['VM']=getNewVM()

    else:
        ResourcesDict['TYPE']="AP"
        ResourcesDict['TAPNAME']=getNewTapPortName()
        ResourcesDict['VM']=getNewVM()

    VMAssociations[entityName]=ResourcesDict
    return ResourcesDict
    

def exec_ssh_command (client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    stderr=stderr.readlines()
    stdout=stdout.readlines()
    stderr.extend(stdout)
    print("stderr="+str(stderr))
    output=""
    for line in stderr:
        output=output+line
    if output!="":
        print(output)
    
    

def sshToMachine(VMIP, VMUser, VMPass):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(VMIP, username=VMUser, password=VMPass)
    return client
    

def addTunnelOnVM_help(VMIP, VMUser, VMPass, TapIP, TapMAC, RemoteIP):
    cmdList=[]
    client=sshToMachine(VMIP, VMUser, VMPass)
    cmdList.append("echo  %s | sudo -S ovs-vsctl del-br br1" % (VMPass))
    cmdList.append("echo  %s | sudo -S  ~/addTunnelOnVM.sh %s %s %s" % (VMPass, RemoteIP, TapIP, TapMAC))
    
    for cmd in cmdList:
        exec_ssh_command(client,cmd)
    client.close()


def connectVMAndDocker(LocalPswd, RemoteIP, BrName, TapPortName, DockerName):
    cmdList=[]
    cmdList.append("echo  %s | sudo -S ovs-vsctl del-br %s" % (LocalPswd, BrName))
    cmdList.append("echo %s| sudo -S ./connectVMAndDocker.sh %s %s %s %s" % (LocalPswd, RemoteIP, BrName, TapPortName, DockerName))
    for cmd in cmdList:
        os.system(cmd)

        
def addTunnelOnStation_help(dockerName, wlanInterfaceName):
    cmdList=[]
    cmdList.append('sudo docker exec -it %s chmod 777 /app/addTunnelOnStation.sh ' % (dockerName) )
    cmdList.append("sudo docker exec -it %s /bin/bash -c \'/app/addTunnelOnStation.sh %s\'" % (dockerName, wlanInterfaceName) )
    for cmd in cmdList:
        os.system(cmd)

def addTunnelOnStation(stationName):
    dockerName=getDockerName(stationName)
    wlanInterfaceName=stationName+"-wlan0"
    addTunnelOnStation_help(dockerName, wlanInterfaceName)

def addTunnelOnVM(entityName, TapIP, TapMAC):
    global VMAssociations
    resources=VMAssociations[entityName]
    
    VMIP=resources['VM'][0]
    VMUser=resources['VM'][1]
    VMPass=resources['VM'][2]
    RemoteIP=getIPAddress()
    addTunnelOnVM_help(VMIP, VMUser, VMPass, TapIP, TapMAC, RemoteIP)

def addTunnelOnAPBridge(LocalPswd, apName, TapPortName, VMIP):
    cmdList=[]
    cmdList.append("sudo ovs-vsctl add-port ap1 %s -- set Interface %s type=gre options:remote_ip=%s" % (TapPortName, TapPortName, VMIP) )
    for cmd in cmdList:
        os.system(cmd)




readVMFile()

def addVMToStation(stationName, TapIPlocal, TapIPRemote, TapMAC):
    global LocalPswd
    resources=getResourcesUsedForVM(stationName,True)
    addTunnelOnVM(stationName, TapIPRemote, TapMAC)
    VMIP=resources['VM'][0]
    BrName=resources['BRNAME']
    print("BrName="+BrName)
    TapPortName=resources['TAPNAME']
    dockerName=getDockerName(stationName)
    connectVMAndDocker(LocalPswd, VMIP, BrName, TapPortName, dockerName)
    addTunnelOnStation(stationName)

def addVMToAP(apName, TapIPRemote):
    global LocalPswd
    resources=getResourcesUsedForVM(apName,False)
    addTunnelOnVM(stationName, TapIPRemote, "")
    VMIP=resources['VM'][0]
    TapPortName=resources['TAPNAME']
    addTunnelOnAPBridge(LocalPswd, apName, TapPortName, VMIP) 


    

addVMToStation("sta1", "172.18.5.6", "172.18.5.5", "00:00:00:00:00:02")
addVMToStation("sta2", "172.18.5.7", "172.18.5.8", "00:00:00:00:00:03")





##addTunnelOnVM("sta1","172.18.5.6", "00:00:00:00:00:02", True)


##addTunnelOnVM("192.168.56.115","vm","vm","172.18.5.5",
##              "00:00:00:01:00:05","192.168.56.114")
##
##connectVMAndDocker("wifi", "192.168.56.115", "172.18.5.6", "br1", "tap1", "mn.sta1")
##        
##addTunnelOnStation("mn.sta1", "sta1-wlan0")




