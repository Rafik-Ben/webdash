'''genindex.py'''
#base data
inet={'img':'img/internet.png',  'head':'Internet',    'text':'Ping: _val_ ms'}
elec={'img':'img/voltage.png',   'head':'Electricity', 'text':'Voltage: _val_ V'}
hwat={'img':'img/hotwater.png',  'head':'Hot water',   'text':'Temperature: _val_ C'}
cwat={'img':'img/coldwater.png', 'head':'Cold water',  'text':'Pressure: _val_ Atm'}
cam1={'img':'img/camera.png',    'head':'Camera',      'text':'Status: _val_'}

def getdata():
	## TODO: get real values
	testdata={'inet':'20', 'volt':'200', 'hwat':'50', 'cwat':'3', 'cam1':'ok'}
	return testdata

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
	print '</body></html>'
	
def printdata(img, head, text, color):
	print '<table width="300" class="tbl" cols="3" frame="border" cellpadding="5"><tr>'
	print '<td class="'+color+'" width="5">&nbsp;</td><td width="64"><img src="'+img+'"></td>'
	print '<td><p class="hd">'+head+'</p><p class="nt">'+text+'</p></td>'
	print '</tr></table><br>'


# Main
data = getdata()
printhead()

## inet
vals=data['inet']
vali=int(vals)
text=inet['text'].replace('_val_', vals)
if vali > 0 and vali < 100:
	color='green'
else:
	color='red'
printdata(inet['img'], inet['head'], text, color)

## volt
vals=data['volt']
vali=int(vals)
text=elec['text'].replace('_val_', vals)
if vali > 210 and vali < 240:
	color='green'
else:
	color='red'
printdata(elec['img'], elec['head'], text, color)

## hwat
vals=data['hwat']
vali=int(vals)
text=hwat['text'].replace('_val_', vals)
if vali > 50 and vali < 90:
	color='green'
else:
	color='red'
printdata(hwat['img'], hwat['head'], text, color)

## cwat
vals=data['cwat']
vali=int(vals)
text=cwat['text'].replace('_val_', vals)
if vali > 2 and vali < 6:
	color='green'
else:
	color='red'
printdata(cwat['img'], cwat['head'], text, color)

## cam1
vals=data['cam1']
text=cam1['text'].replace('_val_', vals)
if vals == 'ok':
	color='green'
else:
	color='red'
printdata(cam1['img'], cam1['head'], text, color)

printtail()
 
 