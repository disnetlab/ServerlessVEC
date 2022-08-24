import os
import time
import subprocess

vehicleState={}
while(True):
    out,error = subprocess.Popen(["docker node ls|tail -n +3|awk '{print $2\",\"$3}'"],
                            stdout=subprocess.PIPE, shell=True).communicate()
    out=str(out)
    out=out[2:-3]
    print(out)
    allVal=out.split("\\n")
    print(allVal)
    flag=0
    for line in allVal:
        if line == '':
            break
        (vehicle,state)=line.split(",")
##        print(vehicle)
##        print(state)
        if vehicle in vehicleState.keys():
            prevState=vehicleState[vehicle]
            print("%s %s %s" %(vehicle, prevState, state))
            if state=="Ready" and prevState=="Down":
##                print("I M inside_____________________--------------")
                flag=1
        else:
            flag=1
        vehicleState[vehicle]=state
        
        
            
    if flag==1:
        os.system("docker service update --force hello-python --detach=false")
    time.sleep(2)
