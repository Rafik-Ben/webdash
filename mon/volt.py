#!/usr/bin/env python
import subprocess
import socket
import time
import syslog
import httplib, urllib

MOSQHOST='mqtt'
MOSQPORT='1883'
SERHOST = '192.168.88.4'
SERPORT = 10001
DEV485 = '/dev/ttyUSB0'
BUFFER_SIZE = 1024

cmd_dev= '#HGHGTMOHPGMO\r'
cmd_ver= '#HGHGITLRJVKN\r'
cmd_bsp= '#HGHGRNMGLONV\r'
cmd_prty='#HGHGUOSKRNLG\r'
cmd_sbit='#HGHGRNIUJUOQ\r'
cmd_len= '#HGHGLIJVQJGR\r'
cmd_alen='#HGHGHUTISROI\r'
cmd_addr='#HGHGPVMIRPTK\r'
cmd_rsdl='#HGHGSRVLLHNK\r'
cmd_tout='#HGHGRUSNOLGI\r'
cmd_tpro='#HGHGNNQGRGTJ\r'
cmd_nu=  '#HGHGQQTVKOLR\r'
cmd_nt=  '#HGHGSNSMJTOQ\r'

cmd_inu1='#HGHGNHNKUQSO\r'
cmd_ini1='#HGHGMMPJLPPN\r'
cmd_ins1='#HGHGRGNHPVJK\r'
cmd_inp1='#HGHGHQGLKUJI\r'
cmd_inq1='#HGHGNSIPGHJG\r'
cmd_cos1='#HGHGHUJHOQNT\r'
cmd_inf= '#HGHGHKILTUGQ\r'

d={ }
d['G'] = "0000"
d['H'] = "0001"
d['I'] = "0010"
d['J'] = "0011"
d['K'] = "0100"
d['L'] = "0101"
d['M'] = "0110"
d['N'] = "0111"
d['O'] = "1000"
d['P'] = "1001"
d['Q'] = "1010"
d['R'] = "1011"
d['S'] = "1100"
d['T'] = "1101"
d['U'] = "1110"
d['V'] = "1111"


def send(command):
## if defined DEV485 - use local serial, else - SERHOST:SERPORT
  if DEV485:
    import serial
    #syslog.syslog("DEV: "+DEV485+", CMD: "+command)
    ser = serial.Serial(DEV485, 9600, timeout=2)
    ser.write(command)
    rd = ser.read(30)
    ser.close()
    #syslog.syslog("GOT: "+rd)
    return rd
  else:
    done = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    for i in range(5):
	try:
            s.connect((SERHOST, SERPORT))
            s.send(command)
            response = s.recv(BUFFER_SIZE)
            done = 1
            break
        except:
            syslog.syslog("Socket error!")
            time.sleep(1)
    s.close()
    if done == 1:
        return response

def decode_owen(rawinput):
    #print 'Decoding:' , rawinput
    r = { }
    if not rawinput:
        syslog.syslog('Empty response from device')
        return ''

    r['raw'] = rawinput.strip()
    if r['raw'][0:1] != '#':
        syslog.syslog('Invalid frame: does not begin with #')
        return
    r['conv']=r['raw'][1:len(r['raw'])]
    for i in d:
        r['conv']=r['conv'].replace(i, d[i])
    #print 'conv', r['conv']

    r['addr']=r['conv'][0:8]
    r['addr']=int(r['addr'], 2)
    #print 'addr', r['addr']

    r['addr2']=r['conv'][8:11]
    #print 'addr2', r['addr2']

    r['req']=r['conv'][11:12]
    #print 'req', r['req']

    r['size']=r['conv'][12:16]
    r['size']=int(r['size'], 2)*8
    #print 'size bits', r['size']

    r['hash']=r['conv'][16:32]
    r['hash']=hex(int(r['hash'], 2))
    #print 'hash', r['hash']

    r['data']=r['conv'][32:32+r['size']]
    #print 'data', r['data']
    r['data_int']=int(r['data'], 2)
    #print 'data_int', r['data_int']
    r['data_hex']=hex(r['data_int'])
    #print 'data_hex', r['data_hex']
    r['data_str']=""
    for i in range(2,len(r['data_hex']),2):
        r['data_str']=chr(int(r['data_hex'][i:i+2], 16))+r['data_str']
    #print 'data_str', r['data_str']
    expn=int(r['data'][1:9], 2)-127
    if expn < 0:
        mant=float(str('1.'+str(int(r['data'][9:32], 2))))
        r['data_float']=str(2**expn*mant)
    else:
	big=int('1'+r['data'][9:9+expn], 2)
	small=int(r['data'][9+expn:32], 2)
	r['data_float']=str(big)+'.'+str(small)

    r['check']=r['conv'][32+r['size']:]
    r['check_hex']=hex(int(r['check'], 2))
    return r

def myround(val):
  return str(int(round(float(val))))

r = send(cmd_inu1)
r = decode_owen(r)
u = myround(r['data_float'])
r = send(cmd_ini1)
r = decode_owen(r)
i = r['data_float']
r = send(cmd_inf)
r = decode_owen(r)
f = r['data_float']
#syslog.syslog("u="+u+", i="+i+", f="+f)

## MQTT
subprocess.call(["mosquitto_pub", "-h", MOSQHOST, "-p", MOSQPORT, "-t", "/sensors/elec/u", "-m", str(u)])
subprocess.call(["mosquitto_pub", "-h", MOSQHOST, "-p", MOSQPORT, "-t", "/sensors/elec/i", "-m", str(i)])
subprocess.call(["mosquitto_pub", "-h", MOSQHOST, "-p", MOSQPORT, "-t", "/sensors/elec/f", "-m", str(f)])

## things speak
TSKEY='thingspeak_api_key'
params = urllib.urlencode({'field1': u, 'field2': i, 'field3': f, 'key': TSKEY})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
#print response.status, response.reason
data = response.read()
conn.close()

