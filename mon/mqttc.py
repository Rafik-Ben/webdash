#!/usr//bin/env python
##import mosquitto (if older mosquitto is used instead of newer paho)
import threading
import time
import pickle
import subprocess

## some constants
data = {}
mqttcid='clientid'
mqtthost='localhost'
mqttport='1883'
fwdhost='cloudmqtt.com'
fwdport='12345'
fwduser='user'
fwdpass='pass'
dumpfile='/tmp/sensors.data'
dumpinterval=300
uploadcmd=['curl', '-s', '-u', 'user:pass', 'ftp://site', '-T', dumpfile]

## Source URL: https://pypi.python.org/pypi/paho-mqtt#usage-and-api

def on_connect(client, userdata, rc):
  if rc == 0:
    client.subscribe("/sensors/#")
  else:
    print "Connection failed: ", rc

def on_message(client, userdata, msg):
  topic=msg.topic.replace('/sensors/','')
  topic=topic.replace('/', '-')
  data[topic] = msg.payload
  print topic,'\t',msg.payload
  fwdcmd=['mosquitto_pub','-h',fwdhost,'-u',fwduser,'-P',fwdpass,'-p',fwdport,'-t',topic,'-m',msg.payload]
  rc=subprocess.call(fwdcmd)

def on_timer(interval):
  ## TODO: save to rrd, update graphs, export to picle, upload all to site
  while True:
    print data
    f=open(dumpfile,'wb')
    pickle.dump(data, f)
    f.close()
    rc=subprocess.call(uploadcmd)
    data.clear()
    #print 'Upload:', rc
    time.sleep(interval)

## Start
t = threading.Thread(target=on_timer, args=(dumpinterval,))
t.daemon = True
t.start()

import paho.mqtt.client as paho
client = paho.Client(mqttcid)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtthost, mqttport, 60 )
rc = 0
while rc == 0:
  rc = client.loop()

print "Exit code: ", rc
