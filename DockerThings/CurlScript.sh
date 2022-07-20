#!/usr/bin/env bash
  
TIMEFORMAT=%R

#curlStatus=$(time curl --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python)
#sed 's/,/;/g' <<<"$curlStatus"
#echo "$curlStatus"

serNo="$1"

#mytime="$(time ( curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python ) 2>&1 1>/dev/null )"
mytime="$(time (curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python) 2>&1)"
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


swarmStatus=$(docker info| grep Swarm| awk '{print $NF}')
#echo "$swarmStatus"

position=$(sed 's/,/;/g' <<<"$position")
mytime=$(sed 's/,/;/g' <<<"$mytime")
echo "${serNo},${status},${swarmStatus},${position}, ${mytime}"

