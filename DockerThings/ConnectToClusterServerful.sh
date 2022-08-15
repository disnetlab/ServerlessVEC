#Add Position in PositionFile
position="$1"
echo "$position">PositionFile

interface="`hostname`-wlan0"
#Check if node connected with RSU
status=$(iw dev "$interface" link| head -n1| awk '{print $1;}')
if [[ "$status" == "Connected" ]];
then
	keepPingingScript=$(ps aux | grep ./KeepPingingServerful.sh | grep -v grep| awk '{print $NF}')
	if [[ "$keepPingingScript" == "" ]];
	then
		./KeepPingingServerful.sh &
		date>test
	fi
fi

if [[ "$2" == "stop" ]];
then
        pid=$(ps aux| grep KeepPingingServerful| grep -v grep| awk '{print $2}')
        kill -9 "$pid"
	date>>test
fi

