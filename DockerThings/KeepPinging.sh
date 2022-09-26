#!/usr/bin/env bash
if mkdir -- lock 2>/dev/null
then
	echo "" > PingLogs
	count=0
	while true
	do
		count=$((count+1))
		# echo ${count}
		sleep 0.3
		timeout 3 ./CurlScript.sh ${count} >> PingLogs & 
	done 
fi

