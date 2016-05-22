'''genindex.py'''
import pickle
import datetime
import os.path
#import subprocess
## base data
newdatafile='sensors.data'
olddatafile='old.data'
failurl='https://maker.ifttt.com/'
okurl='https://maker.ifttt.com/'
res={
'inet-p-img':'img/internet.png',  'inet-p-head':'Internet',    'inet-p-text':'Ping: _val_ ms',
'elec-u-img':'img/voltage.png',   'elec-u-head':'Electricity', 'elec-u-text':'Voltage: _val_ V',
'hwat-t-img':'img/hotwater.png',  'hwat-t-head':'Hot water',   'hwat-t-text':'Temperature: _val_ &deg;C',
'cwat-p-img':'img/coldwater.png', 'cwat-p-head':'Cold water',  'cwat-p-text':'Pressure: _val_ Atm',
'cam1-img'  :'img/camera.png',    'cam1-head':'Camera',      'cam1-text':'Status: _val_',
'env-b-img' :'img/barometer.png', 'env-b-head':'Barometer',    'env-b-text':'Pressure: _val_ mmHg'
}
keys=('inet-p', 'elec-u', 'cwat-p', 'hwat-t', 'env-b', 'cam1')
strkeys=('cam1')

def printhead():
	print '<html><head><style type="text/css">'
	print '.tbl { border: 2px solid black; padding: 5px; width: 400px;}'
	print '.hd { font-size: 20; text-align: left; }'
	print '.nt { font-size: 15; text-align: right; }'
	print '.green { background-color: forestgreen; }'
	print '.yellow { background-color: gold; }'
	print '.red { background-color: red; }'
	print '.gray { background-color: darkgray; }'
	print '</style></head><body>'

def printtail():
	from datetime import datetime
	print '<p>Updated:', str(datetime.now().replace(microsecond=0)), '</p>'
	print '</body></html>'
	
def printdata(img, head, text, color):
	print '<table class="tbl" cols="3" frame="border" cellpadding="5"><tr>'
	print '<td class="'+color+'" width="5">&nbsp;</td><td width="64"><img src="'+img+'"></td>'
	print '<td><p class="hd">'+head+'</p><p class="nt">'+text+'</p></td>'
	print '</tr></table><br>'

def roundFloat(flt):
	return str(int(round(float(flt))))
	
def parseData(key, val):
	if key in strkeys:
		## TODO: handle keys with string values
		return
	else:
		val=roundFloat(val)
		vali=int(val)
		## get trend
		if key in olddata:
			if vali > int(olddata[key]):
				trend='&#8599;' ## arrow up-right
			elif vali < int(olddata[key]):
				trend='&#8600;' ## arrrow down-right
			else:
				trend=''
		## get color
		if key == 'inet-p':
			if vali > 0 and vali < 100:
				return 'green', val, trend
			else:
				return 'red', val, trend
		elif key == 'elec-u':
			if vali > 210 and vali < 240:
				return 'green', val, trend
			else:
				return 'red', val, trend
		elif key == 'hwat-t':
			if vali > 50 and vali < 90:
				return 'green', val, trend
			else:
				return 'red', val, trend
		elif key == 'env-b':
			if vali > 740 and vali < 770:
				return 'green', val, trend
			else:
				return 'red', val, trend
		else:
			## this should draw attention to unknown key
			return 'gray', val

def getData(file):
	if os.path.isfile(file):
		f=open(file,'rb')
		## TODO: check if load ok
		data=pickle.load(f)
		f.close()
	else:
		data=dict()

	return data		

def sendNotify(sensor, failed):
	if falied:
		#rc=subprocess.call(['curl', '-X', 'POST', failurl])
		rc=datetime.now()
	else:
		#rc=subprocess.call(['curl', '-X', 'POST', okurl])
		rc=datetime.now()
	return

	
## Main ###
data=getData(newdatafile)
olddata=getData(olddatafile)
printhead()

## parse list
for k in keys:
	if k in data:
		## if new data arrived - update page and olddata
		val=data[k]
		color,val,tail=parseData(k, val)
		## check if notify needed
		if k+'-failed' in olddata:
			if k+'-failed' == True:
				olddata[k+'-failed']=False
				sendNotify(k, False)
		## save data
		olddata[k]=val
		olddata[k+'-age']=datetime.datetime.now().replace(microsecond=0)
		olddata[k+'-failed']=False
	else:
		color='gray'
		if k in olddata and k+'-age' in olddata:
			## if we have old data - use it and show age at tail
			val=olddata[k]
			tail='('+str(datetime.datetime.now().replace(microsecond=0) - olddata[k+'-age'])+')'
			## send notify
			if k+'-failed' in olddata:
				if k+'-failed' == False:
					olddata[k+'-failed']=True
					sendNotify(k, True)
		else:
			## else - show question marks
			val='no data'
			tail='no age'

	## finally, print data
	img=res[k+'-img']
	head=res[k+'-head']
	text=res[k+'-text'].replace('_val_', val)+'&nbsp;'+tail
	printdata(img, head, text, color)

printtail()
## save old data
f=open(olddatafile,'wb')
pickle.dump(olddata, f)
f.close()
## remove used data
if os.path.isfile(newdatafile):
	os.remove(newdatafile)

## end