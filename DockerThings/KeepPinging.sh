#!/usr/bin/env bash
echo "" > PingLogs
if mkdir -- lock 2>/dev/null
then
	count=0
	while true
	do
		count=$((count+1))
		# echo ${count}
		sleep 0.3
		timeout 3 ./CurlScript.sh ${count} >> PingLogs & 
	done 
fi

