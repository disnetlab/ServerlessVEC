#!/usr/bin/env bash

#STart Docker service if not already running
dockerStatus=$(service docker status| awk '{print $4}')
if [[ "$dockerStatus" == "not" ]];
then
        service docker start
	sleep 1
fi

interface="`hostname`-wlan0"

#Add Position in PositionFile
position="$1"
echo "$position">PositionFile

if [[ "$2" == "stop" ]];
then
        pid=$(ps aux| grep KeepPinging| grep -v grep| awk '{print $2}')
        kill -9 "$pid"
	date>>test
	exit 0
fi

timestep="$2"
echo "$timestep">TimestepFile


#Check if node connected with RSU
status=$(iw dev "$interface" link| head -n1| awk '{print $1;}')
if [[ "$status" == "Connected" ]];
then
        #If node connected with RSU, join the docker swarm
        swarmStatus=$(docker info| grep Swarm| awk '{print $NF}')
        if [[ "$swarmStatus" == "inactive" ]];
        then
                cmd=$(curl 172.18.5.12:5000)
                bash -c "$cmd"
        fi

        #STart the KeepPinging Script to log the response timnes
        swarmStatus=$(docker info| grep Swarm| awk '{print $NF}')
        if [[ "$swarmStatus" == "active" ]];
        then
                keepPingingScript=$(ps aux | grep KeepPinging.sh | grep -v grep| awk '{print $NF}')
                if [[ "$keepPingingScript" == "" ]];
                then
			date>test
                        ./KeepPinging.sh &
                fi
        fi
fi


