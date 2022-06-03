#! /bin/bash
rasp='https://salins.btssnir.lycee-costebelle.fr/api/values.php' #sur le réseau
#rasp='192.168.0.120/api/values.php' # sur le réseau local
while [ 1 ]
do

echo "rasp="$rasp

# Check if there is sensor data arrive at /var/iot/channels/ every 5 seconds
CID=`ls /var/iot/channels`
echo "CID="$CID
    if [ -n "$CID" ] 
    then
        for channel in $CID
        do
            echo "channel="${#channel}

            com=`awk -F, '{print $3}' /var/iot/channels/$channel`
            echo "channel="$channel
            echo "com="$com
            curl -X POST -d "$com&balise_id=$channel" $rasp
            echo "c'est fé"
            echo "**************"

        done
    else
        echo "empty"
    fi
echo "**************"
echo "**************"
echo "**************"
sleep 1

done

