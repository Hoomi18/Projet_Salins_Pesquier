#! /bin/bash
rasp='192.168.0.120/api/values.php'

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
    
        com=`awk -F, '{print $3}' /var/iot/channels/$channel`
        echo "channel="$channel
        echo "com="$com
        curl -X POST -d "&balise_id=$CID" $rasp
        echo "c'est fé"
        done
    else
        echo "empty"
    fi
echo "**************"
echo "**************"
echo "**************"

sleep 1
done

