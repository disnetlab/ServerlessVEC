netconvert --type-files osmNetconvert.typ.xml,osmNetconvertUrbanDe.typ.xml,osmNetconvertPedestrians.typ.xml,osmNetconvertBicycle.typ.xml,osmNetconvertBicycle.typ.xml,osmNetconvertShips.typ.xml,osmNetconvertRailUsage.typ.xml,osmNetconvertBidiRail.typ.xml,osmNetconvertAirport.typ.xml  --osm-files map.osm --output-file melbcbd.net.xml --geometry.remove --roundabouts.guess --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join

polyconvert --net-file melbcbd.net.xml --osm-files map.osm -o melbcbd.poly.xml

/usr/share/sumo/tools/randomTrips.py -n melbcbd.net.xml -r routes.rou.xml -o trips.xml -e 120  --insertion-rate "$1" 

sumo -c simple.sumocfg  --fcd-output sumoTrace.xml

sudo python3 Simulation/simulation.py sumoTrace.xml melbcbd.net.xml 0
