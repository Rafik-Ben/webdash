import mosquitto
import threading
import time
import pickle
import subprocess

## some constants
data = {}
mqttcid='eeepc'
dumpfile='/tmp/sensors.data'
dumpinterval=300
uploadcmd=['ftp-upload', '-h', 'HOST', '-u', 'USER', '--password', 'PASSWORD', '--passive', '-b', dumpfile]
mqttserver='SERVER'
mqttport='PORT'
mqtttout=60

client = mosquitto.Mosquitto(mqttcid)
## Source URL: https://pypi.python.org/pypi/paho-mqtt#usage-and-api

def on_connect(obj, rc):
  if rc == 0:
    client.subscribe("/sensors/+")
  else:
    print "Connection failed: ", rc

def on_message(obj, msg):
  topic=msg.topic.replace('/sensors/','')
  data[topic] = msg.payload
  print topic, msg.payload

def on_timer(interval):
  ## TODO: save to rrd, update graphs, export to picle, upload all to site
  while True:
    #print data
    f=open(dumpfile,'wb')
    pickle.dump(data, f)
    f.close()
    rc=subprocess.call(uploadcmd)
    data.clear()
    print 'Upload:', rc
    time.sleep(interval)

## Start
t = threading.Thread(target=on_timer, args=(dumpinterval,))
t.daemon = True
t.start()

client = mosquitto.Mosquitto(mqttcid)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttserver, mqttport, mqtttout)
rc = 0
while rc == 0:
  rc = client.loop()

print "Exit code: ", rc


