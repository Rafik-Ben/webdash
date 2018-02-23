#!/bin/sh
LOG=/media/1TB/www/pingtest.log
IMG=/media/1TB/www/pingtest.png
ADDR=213.180.193.3
MOSQ='mqtt'
TMP=/tmp/pingtest
REC=1440
PINGMAX=100
LASTPTS=20
ERRLVL=50
FAILLVL=50
APIKEY=thingspeak_api_key

##get data
DATE=`date +%Y/%m/%d-%H:%M | tr '\n' ' '`

pingav(){
  ping $1 -c 3 1> $TMP 2>/dev/null
  res=$?
  if [ "$res" = "0" ]; then
    AV=`cat $TMP | grep rtt | awk '{print $4}' | awk 'BEGIN { FS = "/" } ; { print $2 }'`
    AV=`echo $AV|awk -F . '{print $1}'`
    [ "$AV" -gt "$PINGMAX" ] && AV=$PINGMAX
    ER=0
  else
    AV=0
    ER=$ERRLVL
  fi
  rm $TMP
}

## yandex
pingav $ADDR
PING1=$AV
mosquitto_pub -h $MOSQ -p 1883 -t /sensors/inet/p -m $PING1

## balcony camera
pingav 192.168.88.8
PING2=$AV
mosquitto_pub -h $MOSQ -p 1883 -t /sensors/cam1/p -m $PING2

## hall camera
pingav 192.168.88.7
PING3=$AV
mosquitto_pub -h $MOSQ -p 1883 -t /sensors/cam2/p -m $PING3

## Trendnet
pingav 192.168.88.11
PING4=$AV
#no need for mqtt 

## all pings to thingspeak
wget -q -O /dev/null "https://api.thingspeak.com/update?api_key=$APIKEY&field1=$PING1&field2=$PING2&field3=$PING3&field4=$PING4"


exit 0
# get status
MEAN=`tail -n $LASTPTS /media/1TB/www/pingtest.log |awk '{ print $4}'`
sum=0
for i in $MEAN; do
  sum=$(( sum + i ))
done
MEAN=$(( sum / $LASTPTS ))
MEAN=`echo $MEAN | awk -F. '{print $1}'`
DIFF=$(( AV - MEAN ))
## TODO: use total diff sum for compare
if [ "$MEAN" -lt "$FAILLVL" ]; then
  STATUS="OK"
else
  STATUS="FAIL"
  ER=$ERRLVL
fi

ST="LAST: $AV, DIFF: $DIFF, MEAN: $MEAN, STATUS: $STATUS, ROUTER: $AV2"
echo "$DATE $AV $ER $DIFF $MEAN $AV2" >> $LOG

##remove old
tail -n $REC $LOG > $LOG.tmp
mv $LOG.tmp $LOG


exit 0
##recreate image
#set title "Ping to $ADDR. $ST"
## error with boxes, not lines
gnuplot <<END
set terminal png size 800,300
set output "$IMG"
set xdata time
set timefmt "%Y/%m/%d-%H:%M"
set grid
set ylabel "Delay (ms)"
set xlabel "Ping to $ADDR. $ST"
set format x "%H:%M"
set time
set key top left
plot [*:*][*:*] "$LOG" using 1:3 with lines title "ERROR", \
"$LOG" using 1:2 with lines title "$ADDR", \
"$LOG" using 1:4 with lines title "diff", \
"$LOG" using 1:5 with lines title "mean diff"

END
