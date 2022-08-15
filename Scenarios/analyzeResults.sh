#!/bin/bash

for i in */;
do
	echo $i;
	cd $i
	echo -n "Info: "
	cat Info
	echo "Serverless:"
	cd Serverless
	responseTimesAggr=""
	for j in Log*;
	do 
		echo $j
		#cat $j| awk -F',' '{print $6}'
		cat $j| cut -d',' -f6
		responseTimes=$(cat $j| cut -d',' -f6)
		#responseTimes=$(cat $j| awk -F',' '{print $6}')
		echo -e ${responseTimes}
		responseTimesAggr=$(paste <(echo "$responseTimesAggr") <(echo "$responseTimes") --delimiters '')
	done
	cd ..
	cd ..
done
