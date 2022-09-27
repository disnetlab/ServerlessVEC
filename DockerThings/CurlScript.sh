#!/usr/bin/env bash
  
TIMEFORMAT=%R

#curlStatus=$(time curl --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python)
#sed 's/,/;/g' <<<"$curlStatus"
#echo "$curlStatus"

serNo="$1"

response="$(time (curl -s --max-time 3 --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python) 2>timetemp)"
if [ -z "$response" ]
then
        response="Unsucc"
else
        response="Succesful"
fi

#echo "$mytime"

mytime=$(head -n 1 timetemp)
#echo "$mytime"


interface="`hostname`-wlan0"
status=$(iw dev "$interface" link| head -n1| awk '{print $1;}')
if [[ "$status" != "Connected" ]];
then
        status="NotConnected"
fi
#echo "$status"

position=$(head -n 1 PositionFile)
#echo "$position"

timestep=$(head -n 1 TimestepFile)
#echo "$timestep"

hostname=$(hostname)


swarmStatus=$(docker info 2>/dev/null| grep Swarm| awk '{print $NF}')
#echo "$swarmStatus"

position=$(sed 's/,/;/g' <<<"$position")
mytime=$(sed 's/,/;/g' <<<"$mytime")
response=$(sed 's/,/;/g' <<<"$response")
echo "${serNo},${hostname}, ${status},${swarmStatus},${position}, ${response}, ${timestep}, ${mytime}"

