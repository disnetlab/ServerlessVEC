#!/usr/bin/env bash
echo "" > PingLogs
count=0
while true
do
        count=$((count+1))
        echo ${count}
        sleep 0.5
        ./CurlScript.sh ${count} >> PingLogs  
done 

