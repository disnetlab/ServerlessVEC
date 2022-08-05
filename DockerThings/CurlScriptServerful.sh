#!/usr/bin/env bash
  
TIMEFORMAT=%R
serNo="$1"

response="$(time (curl -s --form "image_file=@abc.jpg"  http://172.18.5.12:8080/function/hello-python) 2>timetemp)"
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

position=$(sed 's/,/;/g' <<<"$position")
mytime=$(sed 's/,/;/g' <<<"$mytime")
response=$(sed 's/,/;/g' <<<"$response")

echo "${serNo},${status},${position}, ${response}, ${mytime}"

