#!/usr/bin/env bash
echo "" > PingLogs
count=0
while true
do
        count=$((count+1))
        echo ${count}
        sleep 2
        ./CurlScriptServerful.sh ${count} >> PingLogs &
done