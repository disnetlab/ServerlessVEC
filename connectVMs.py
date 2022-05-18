import paramiko
import os
import subprocess

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
    


def addTunnelOnVM(VMIP, VMUser, VMPass, TapIP, TapMAC, RemoteIP):
    cmdList=[]
    client=sshToMachine(VMIP, VMUser, VMPass)
    cmdList.append("sudo ovs-vsctl del-br br1" % (VMPass))
    cmdList.append("sudo /home/wifi/Desktop/ConnectedCars/VMSideTunnel.sh %s %s %s" % (VMPass, RemoteIP, TapIP, TapMAC))
    
    for cmd in cmdList:
        exec_ssh_command(client,cmd)
    client.close()


def connectVMAndDocker(LocalPswd, RemoteIP, TapIP, BrName, TapPortName, DockerName):
    cmdList=[]
    cmdList.append("echo  %s | sudo -S ovs-vsctl del-br %s" % (LocalPswd, BrName))
    cmdList.append("echo %s| sudo -S ./connectVMAndDocker.sh %s %s %s %s %s" % (LocalPswd, RemoteIP, TapIP, BrName, TapPortName, DockerName))
    for cmd in cmdList:
        os.system(cmd)
        
def addTunnelOnStation(dockerName, wlanInterfaceName):
    cmdList=[]
    cmdList.append('sudo docker exec -it %s chmod 777 /app/addTunnelOnStation.sh ' % (dockerName) )
    cmdList.append("sudo docker exec -it %s /bin/bash -c \'/app/addTunnelOnStation.sh %s\'" % (dockerName, wlanInterfaceName) )
    for cmd in cmdList:
        os.system(cmd)

    
##addTunnelOnVM("192.168.56.115","vm","vm","172.18.5.5",
##              "00:00:00:01:00:05","192.168.56.114")

connectVMAndDocker("wifi", "192.168.56.115", "172.18.5.6", "br1", "tap1", "mn.sta1")
        
addTunnelOnStation("mn.sta1", "sta1-wlan0")




