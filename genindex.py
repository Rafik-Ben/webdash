'''genindex.py'''
import pickle
## base data
dumpfile='=== UPLOADED DUMP FILE ==='
res={
'inet-img':'img/internet.png',  'inet-head':'Internet',    'inet-text':'Ping: _val_ ms',
'elec-img':'img/voltage.png',   'elec-head':'Electricity', 'elec-text':'Voltage: _val_ V',
'hwat-img':'img/hotwater.png',  'hwat-head':'Hot water',   'hwat-text':'Temperature: _val_ &deg;C',
'cwat-img':'img/coldwater.png', 'cwat-head':'Cold water',  'cwat-text':'Pressure: _val_ Atm',
'cam1-img':'img/camera.png',    'cam1-head':'Camera',      'cam1-text':'Status: _val_',
'baro-img':'img/barometer.png', 'baro-head':'Barometer',    'baro-text':'Pressure: _val_ mmHg'
}

def getdata():
	f=open(dumpfile,'rb')
	data=pickle.load(f)
	f.close()
	return data

def printhead():
	print '<html><head><style type="text/css">'
	print '.tbl { border: 1px solid black; padding: 5px; }'
	print '.hd { font-size: 20; text-align: left; }'
	print '.nt { font-size: 15; text-align: right; }'
	print '.green { background-color: forestgreen; }'
	print '.yellow { background-color: gold; }'
	print '.red { background-color: red; }'
	print '.gray { background-color: darkgray; }'
	print '</style></head><body>'

def printtail():
	## time
	from datetime import datetime
	print '<p>Updated:', str(datetime.now()), '</p>'
	print '</body></html>'
	
def printdata(img, head, text, color):
	print '<table width="300" class="tbl" cols="3" frame="border" cellpadding="5"><tr>'
	print '<td class="'+color+'" width="5">&nbsp;</td><td width="64"><img src="'+img+'"></td>'
	print '<td><p class="hd">'+head+'</p><p class="nt">'+text+'</p></td>'
	print '</tr></table><br>'


## Main
data = getdata()
printhead()

## inet
vals=data['inet-p']
vali=int(vals)
text=res['inet-text'].replace('_val_', vals)
if vali > 0 and vali < 100:
	color='green'
else:
	color='red'
printdata(res['inet-img'], res['inet-head'], text, color)

## elec
vals=data['elec-u']
vali=int(round(float(vals)))
text=res['elec-text'].replace('_val_', vals)
if vali > 210 and vali < 240:
	color='green'
else:
	color='red'
printdata(res['elec-img'], res['elec-head'], text, color)

## hwat
vali=int(round(float(data['hwat-t'])))
vals=str(vali)
text=res['hwat-text'].replace('_val_', vals)
if vali > 50 and vali < 90:
	color='green'
else:
	color='red'
printdata(res['hwat-img'], res['hwat-head'], text, color)

## baro
vals=data['env-b']
vali=int(vals)
text=res['baro-text'].replace('_val_', vals)
if vali > 740 and vali < 770:
	color='green'
else:
	color='red'
printdata(res['baro-img'], res['baro-head'], text, color)

## cwat
#vals=data['cwat']
#vali=int(vals)
#text=res['cwat-text'].replace('_val_', vals)
#if vali > 2 and vali < 6:
#	color='green'
#else:
#	color='red'
#printdata(res['cwat-img'], res['cwat-head'], text, color)

## cam1
#vals=data['cam1']
#text=res['cam1-text'].replace('_val_', vals)
#if vals == 'ok':
#	color='green'
#else:
#	color='red'
#printdata(res['cam1-img'], res['cam1-head'], text, color)

printtail()
