#!/bin/bash
export PATH="$PATH:bin:onos/bin"

SSH_KEY=$(cut -d\  -f2 ~/.ssh/id_rsa.pub)



# Create ONOS cluster using ONOS docker image
ONOS_IMAGE=onosproject/onos:1.15.0
for i in {1..1}; do
    echo "Setting up onos-$i..."
    docker container run --detach --name onos-$i --hostname onos-$i --restart=always $ONOS_IMAGE
done

function waitForStart {
    sleep 5
    for i in {1..1}; do
        echo "Waiting for onos-$i startup..."
        ip=$(docker container inspect onos-$i | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
        for t in {1..60}; do
            curl --fail -sS http://$ip:8181/onos/v1/applications --user onos:rocks 1>/dev/null 2>&1 && break;
            sleep 1;
        done
        onos $ip summary >/dev/null 2>&1
    done
}

# Extract the IP addresses of the ONOS nodes
OC1=$(docker container inspect onos-1 | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
#OC2=$(docker container inspect onos-2 | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
#OC3=$(docker container inspect onos-3 | grep \"IPAddress | cut -d: -f2 | sort -u | tr -d '", ')
#ONOS_INSTANCES="$OC1 $OC2 $OC3"

waitForStart

#echo "Activating OpenFlow and ProxyARP applications..." $OC1
#onos $OC1 app activate org.onosproject.openflow proxyarp layout
#onos $OC1

