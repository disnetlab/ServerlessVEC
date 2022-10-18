#!/usr/bin/env bash
  
TIMEFORMAT=%R

#curlStatus=$(time curl --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python)
#sed 's/,/;/g' <<<"$curlStatus"
#echo "$curlStatus"

serNo="$1"

timestampbefore=$(date +%s%3N)
start_time=$(date +%s.%3N)
response=$(curl -s --max-time 3 --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python 2>&1)
end_time=$(date +%s.%3N)
timestampafter=$(date +%s%3N)
temp_response="$(echo ${response}| grep confidence)"
if [ -z "$temp_response" ]
then
        response1="Unsucc"
else
        response1="Succesful"
fi

#echo "$mytime"

elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
#mytime=$(head -n 1 timetemp)
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
elapsed=$(sed 's/,/;/g' <<<"$elapsed")
response=$(sed 's/,/;/g' <<<"$response")

echo "${serNo}, ${response}","==============" >> responseLogs
echo "${serNo},${hostname}, ${status},${swarmStatus},${position},  ${timestep}, ${timestampbefore}, ${timestampafter}, ${elapsed}, ${response1}"

