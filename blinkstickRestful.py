#!c:\python27\python.exe

#from numpy import random
import random, time
from threading import Thread
from blinkstick import blinkstick
from flask import Flask, json, request
#from threading import Lock for another day/time


def print_info(stick):
    print("Found device:")
    device=stick.get('device')
    print("    Manufacturer:  {0}".format(device.get_manufacturer()))
    print("    Description:   {0}".format(device.get_description()))
    print("    Variant:       {0}".format(device.get_variant_string()))
    print("    Serial:        {0}".format(device.get_serial()))
    print("    Mode:          {0}".format(device.get_mode()))
    if device.get_variant() == blinkstick.BlinkStick.BLINKSTICK_FLEX:
        print("    LED conf:      {0}".format(stick.get('maxLed')))
    print("    Info Block 1:  {0}".format(device.get_info_block1()))
    print("    Info Block 2:  {0}".format(device.get_info_block2()))
    
def max_leds(stick):
    count=-1
    try:
        count = stick.get_led_count()
    except:
        count = 32
    return count
    
def getRandomColor():
    r=int(random.random() *256)
    g=int(random.random() *256)
    b=int(random.random() *256)
    return r,g,b
    
def getStick(args):
    serial=args.get('deviceId')
    return devices[serial]

def getColorParams(args):
    r=int(args.get('r'))
    g=int(args.get('g'))
    b=int(args.get('b'))
    stick=getStick(args)
    return stick,r,g,b
    
def list():
    return devices.keys()
    
def setIndexedColor(stick,index,r,g,b):
    device=stick.get('device')
    index=int(index)
    device.set_color(red=applyBrightness(stick,r),green=applyBrightness(stick,g),blue=applyBrightness(stick,b),index=index)
    stick.get('colors')[index]={
                                'r':r, 
                                'g':g, 
                                'b':b
                                }
                                
def setStripColors(device,payload):
    device.set_led_data(0, payload)
    
def setStripColor(stick,r,g,b):
    device=stick.get('device')
    maxLED=stick.get('maxLed')
    setStripColors(device,[applyBrightness(stick,g), applyBrightness(stick,r), applyBrightness(stick,b)]*maxLED)
    stick['colors']=[{
                'r':r, 
                'g':g, 
                'b':b}]*maxLED
                
def setStripRandomLEDColors(stick):
    device=stick.get('device')
    maxLED=stick.get('maxLed')
    buffer=[]
    commandBuffer=[]
    for i in range(0,maxLED):
        r,g,b=getRandomColor()
        buffer.append({
                'r':r, 
                'g':g, 
                'b':b})
        commandBuffer.append(applyBrightness(stick,g))
        commandBuffer.append(applyBrightness(stick,r))
        commandBuffer.append(applyBrightness(stick,b))
    setStripColors(device,commandBuffer)
    
    stick['colors']=buffer
    
def setStripLEDColors(stick,payload):
    device=stick.get('device')
    maxLED=stick.get('maxLed')
    buffer=[]
    commandBuffer=[]
    for i in range(0,maxLED):
        r=payload[i]['r']
        g=payload[i]['g']
        b=payload[i]['b']
        buffer.append({
                'r':r, 
                'g':g, 
                'b':b})
        commandBuffer.append(applyBrightness(stick,g))
        commandBuffer.append(applyBrightness(stick,r))
        commandBuffer.append(applyBrightness(stick,b))
    setStripColors(device,commandBuffer)
    
    stick['colors']=buffer
    
def applyBrightness(stick,rgb):
    brightness=stick.get('brightness')
    return int(rgb*brightness)
    
def setBrightness(stick,brightness):
    device=stick.get('device')
    commandBuffer=[]
    stick['brightness']=brightness
    for color in stick.get('colors'):
        commandBuffer.append(applyBrightness(stick,color.get('g')))
        commandBuffer.append(applyBrightness(stick,color.get('r')))
        commandBuffer.append(applyBrightness(stick,color.get('b')))
    
    setStripColors(device,commandBuffer)

def playanimation(stick,delay,stripCommands):
    for i in range(0,len(stripCommands)):
        content=stripCommands[i]
        setStripLEDColors(stick,content)
        if(stick['animationThread']=="Stopping"):
            raise StopIteration
        time.sleep(delay / 1000.0)
    
def startAnimation(stick,delay,count,persistent,stripCommands):
    try:
        if count > 0:
            for loopi in range(0,count):
                playanimation(stick,delay,stripCommands)
        else:
            while(True):
                playanimation(stick,delay,stripCommands)
    except StopIteration:
        print "Caught"
    if not (persistent.lower() == "true"):
        setStripColor(stick,0,0,0) # prevent staying in last state
    stick['animationThread']="Stopped"
    

def main():
    global devices
    devices={}
    detectedSources = blinkstick.find_all()
    for device in detectedSources:
        maxLED=max_leds(device)
        devices[device.get_serial()]={
            'maxLed':maxLED,
            'device':device,
            'colors':[{
                'r':0, 
                'g':0, 
                'b':0}]*maxLED,
            'brightness':1,
            'animationThread':"Stopped"
        }
        setStripColor(devices[device.get_serial()],0,0,0)
        print_info(devices[device.get_serial()])

    api = Flask(__name__)

    @api.route('/list', methods=['GET'])
    def get_devices():
      return json.dumps(list())
      
    @api.route('/setColor', methods=['GET'])
    def set_one_color():
        try:
            stick,r,g,b=getColorParams(request.args)
            
            if("index" in request.args):
                setIndexedColor(stick,request.args.get('index'),r,g,b)
            else:
                setStripColor(stick,r,g,b)
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/setColors', methods=['POST'])
    def set_strip_colors():
        try:
            stick=getStick(request.args)
            content=request.json
            setStripLEDColors(stick,content)
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/setRandom', methods=['GET'])
    def set_random_same_color():
        try:
            stick=getStick(request.args)
            r,g,b=getRandomColor()
            if("index" in request.args):
                setIndexedColor(stick.get('device'),request.args.get('index'),r,g,b)
            else:
                setStripColor(stick,r,g,b)
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})

    @api.route('/getColor', methods=['GET'])
    def get_all_colors():
        try:
            stick=getStick(request.args)
            colors=stick.get('colors')
            if("index" in request.args):
                return json.dumps({"success":True,"color":colors.get(request.args.get('index'))})
            else:
                return json.dumps({"success":True,"colors":colors})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/setAllRandom', methods=['GET'])
    def set_random_individual_color():
        try:
            stick=getStick(request.args)
            setStripRandomLEDColors(stick)
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})

    @api.route('/setBrightness', methods=['GET'])
    def set_brightness():
        try:
            stick=getStick(request.args)
            brightness=float(request.args.get('percent'))
            setBrightness(stick,brightness)
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/startAnimation', methods=['POST'])
    def start_animation():
        try:
            stick=getStick(request.args)
            animationContent=request.json
            delay=animationContent['delay']
            count=animationContent['count']
            persistent=animationContent['persistent']
            stripCommands=animationContent['commands']
            if not(stick.get('animationThread') == "Stopped"):
                return json.dumps({"success":False,"error":"Animation is currently " + stick.get('animationThread') + ", cancel with /stopAnimation"})
            
            thread = Thread(target = startAnimation, args = (stick,delay,count,persistent,stripCommands, ))
            thread.start()
            stick['animationThread']="Running"
            
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/stopAnimation', methods=['GET'])
    def stop_animation():
        try:
            stick=getStick(request.args)
            if not(stick.get('animationThread') == "Stopped"):
                stick['animationThread']="Stopping"
            while not (stick.get('animationThread') == "Stopped"):
                status="waiting to stop"
            return json.dumps({"success":True})
        except Exception as error:
            return json.dumps({"success":False,"error":str(error)})
            
    @api.route('/web', methods=['GET'])
    def show_demo_page():
        return """
        <html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Testing platform</title>
<style>

html,body {
	background:#0d4d2b;
}

.whitebg{
	background:white;
}

.group {
	display:block;
	width:(100% - 10px);
	height:auto;
	min-height:40px;
	padding:5px;
}

input[type="color"] {
    -webkit-appearance: none;
    border: solid 0px #11ef88;
    width: 20px;
    height: 20px;
    padding: 0;
    margin: 0;
    display: block;
    float: left;
}

input[type="color"]::-webkit-color-swatch-wrapper {
	padding:0;
	margin:0;
	border: solid 0px transparent;
	border-radius: 40px;
}


</style>
<script>

waiting=false;
lastUrl=""
function pendingCheck(responseText)
{
	insaneFramerate(false);
	waiting=false;
	if(lastUrl!="")
	{
		httpGetAsync(lastUrl, pendingCheck)
		lastUrl="";
	}
}

function httpGetAsync(theUrl, callback)
{
	if(waiting==false)
	{
		waiting=true;
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.onreadystatechange = function() { 
			if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
				callback(xmlHttp.responseText);
		}
		xmlHttp.open("GET", theUrl, true); // true for asynchronous 
		xmlHttp.send(null);
	}
	else
	{
		lastUrl=theUrl;
	}
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function fireColorChange(id,hex)
{
	rgb=hexToRgb(hex)
	if(id=="all")
	{
		httpGetAsync("/setColor?deviceId=BS036121-3.1&r=" + rgb['r'] + "&g=" + rgb['g'] + "&b=" + rgb['b'],pendingCheck);
		/*inputs = document.getElementsByTagName('input');
		for (index = 0; index < inputs.length; ++index) {
			if(inputs[index].getAttribute('type')=='color')
			{
				inputs[index].value=hex;
			}
		}*/
		document.getElementById('all').style.opacity=1;
	}
	else
	{
		httpGetAsync("/setColor?deviceId=BS036121-3.1&r=" + rgb['r'] + "&g=" + rgb['g'] + "&b=" + rgb['b'] + "&index=" + id ,pendingCheck);
		document.getElementById('all').style.opacity=0.5;
	}
}

function componentToHex(c) {
	if(c > 255)
	{
		c=255;
	}
	if(c < 0)
	{
		c=-1;
	}
	  var hex = c.toString(16);
	  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(point)
{
    r=componentToHex(point['r']);
	g=componentToHex(point['g']);
	b=componentToHex(point['b']);
	return "#" + r + g + b;
}

function httpGetAsyncSpecial(theUrl, callback)
{
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
		{
			callback(xmlHttp.responseText);
		}
	}
	xmlHttp.open("GET", theUrl, true); // true for asynchronous 
	try
	{
		xmlHttp.send(null);
	}
	catch(e)
	{
		callback("");
	}
}

function colorCheck(responseText)
{
	var points = JSON.parse(responseText)["colors"];
    for (id = 0; id < points.length; id++) {
		document.getElementById(id).value=rgbToHex(points[id]);
	}
	
}

framerate=1000;
function insaneFramerate(really)
{
	if(really)
	{
		framerate=1;
	}
	else{
		framerate=1000;
	}
}

function colorCheckLoop()
{
	httpGetAsyncSpecial('/getColor?deviceId=BS036121-3.1', colorCheck)
	setTimeout(colorCheckLoop,framerate);
}

function allOn()
{
	httpGetAsyncSpecial("/setColor?deviceId=BS036121-3.1&r=255&g=255&b=255" ,pendingCheck);
}
function allOff()
{
	httpGetAsyncSpecial("/setColor?deviceId=BS036121-3.1&r=0&g=0&b=0" ,pendingCheck);
}
function allRandom()
{
	httpGetAsyncSpecial("/setRandom?deviceId=BS036121-3.1" ,pendingCheck);
}

function allMultiRandom()
{
	httpGetAsyncSpecial("/setAllRandom?deviceId=BS036121-3.1" ,pendingCheck);
}

function setBrightness(value)
{
	httpGetAsync("/setBrightness?deviceId=BS036121-3.1&percent=" + (value/100),pendingCheck);
}

</script>

</head>
<body onload="colorCheckLoop()">
<div class="group">
    <input type="color" id="all" name="all" value="#000000" oninput="fireColorChange(this.id,this.value);">
    <label for="all">All</label>
</div>
<div class="group">
	<input type="range" min="1" max="100" value="5" name="myPercent" oninput="setBrightness(this.value)">
	<label for="myPercent">Brightness</label>
</div>
<div class="group">
	<input type="color" id="0" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="1" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="2" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="3" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="4" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="5" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="6" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="7" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="8" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="9" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="10" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="11" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="12" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="13" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="14" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="15" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="16" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="17" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="18" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="19" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="20" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="21" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="22" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="23" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="24" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="25" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="26" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="27" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="28" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="29" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="30" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="31" value="#000000" oninput="fireColorChange(this.id,this.value);">
</div>
<div class="group whitebg">
	<button onclick="allOn()">All White</button><br/>
	<button onclick="allOff()">All Off/black</button><br/>
	<button onclick="allRandom()">All (one) Random</button><br/>
	<button onclick="allMultiRandom()">All (multiple) Random</button><br/>
</div>

</body>
</html>
"""
            
    api.run(host='0.0.0.0',port=80)
      
        
    

    



if __name__ == '__main__':
    main()