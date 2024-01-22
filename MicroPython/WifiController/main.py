from microdot_asyncio import Microdot, Response, send_file,redirect
from microdot_asyncio_websocket import with_websocket
from machine import Pin,PWM
import json
import uasyncio
import asyncio
import socket
import os

import time
import network
wlan = network.WLAN(network.STA_IF) # create station interface
SERVER_IP='192.168.4.1'

print(wlan.ifconfig()  )
# Initialize MicroDot
app = Microdot()
#Response.default_content_type = 'text/html'
### Motor
MotorPinIN1=Pin(14,Pin.OUT)
MotorPinIN2=Pin(15,Pin.OUT)
MotorPinIN1.off()   #off- forward on -Backword

MotorSpeed=PWM(Pin(15,Pin.OUT))
MotorSpeed.freq(400)
MotorSpeed.duty_u16(00000)

##
servo=PWM(Pin(13))
servo.freq(50)

#params for:
# HD-1440A
#servoPosMid=2500
#servoPosMax=servoPosMid+700
#servoPosMin=servoPosMid-700  #Mid

# GH-S37D
#servoPosMid=4512
#servoPosMax=7000
#servoPosMin=2024  
servoPosMid=4700
servoPosMax=6800
servoPosMin=2600

config = {
  "servoPosMid": servoPosMid,
  "servoPosMax": servoPosMax,
  "servoPosMin": servoPosMin
}

#Configuration File
configFile= 'config.json'

#If file exists read it if not create it with defailt values
if configFile in os.listdir(): 
    f = open(configFile, 'r')
    js=json.loads(f.read())
    servoPosMid=js['servoPosMid']
    servoPosMax=js['servoPosMax']
    servoPosMin=js['servoPosMin']
    f.close()
else:
    f = open(configFile, 'w')
    f.write(json.dumps(config))
    f.flush()
    f.close()


range_steps=(servoPosMax-servoPosMid)/1024.0

servo.duty_u16(servoPosMid)


led = machine.Pin("LED", machine.Pin.OUT)
led.off()                 # set pin to "on" (high) level


# root route
@app.get('/')
def index(request):
    return send_file('/static/index.html')

@app.get('/hotspot-detect.html')
def apple_captive(request):
     #return redirect('/')
     return '<!DOCTYPE HTML><HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>', 200

@app.errorhandler(404)
def not_found(request):
    #return {'error': 'resource not found'}, 404
    #print(request)
    return send_file('/static/index.html')
    

#The socket needs flow-control if not the input buffer wil be flooded
#The web-client must wait for reply before sending more data
@app.route('/ws')
@with_websocket
async def ws(request, ws):
    c = 0
    old_x_position = 9999
    old_y_position = 9999
    led.on()
    servo.duty_u16(servoPosMid)               # sservoPosMid=2500
    print("------------------  WS Connect -----------------")
    while True:
        data = await ws.receive()
        if(type(data) is str) :
            #print(data)
            jsonRecievedData=json.loads(data)
            xPos=jsonRecievedData['xPos']    # Get the xPos element fro the JSON dataobj
            yPos=jsonRecievedData['yPos']    # Get the xPos element fro the JSON dataobj
            
            if(type(xPos) is int) :         #check if data is a int (recieved properly)                   
               #print(f"xPos {xPos}") # Debug data
               if(old_x_position != xPos):
                   old_x_position = xPos
                   turnWheel(xPos)        #Move steering-wheels

            if(type(yPos) is int) :         #check if data is a int (recieved properly)                   
               #print(f"yPos {yPos}") # Debug data
               if(old_y_position != yPos):
                   old_y_position = yPos
                   motorSpeed(yPos)
               
            data = '{}_{}'.format(data, 'ack')        # Echo response
            await ws.send(data)          # send ack to recieve more data

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    #print(path)
    return send_file("static/" + path)

#Turn the car to the left/right
#valid numbers is from -1024 to +1024

def turnWheel(position) :
    
    servo_position=servoPosMid+int(range_steps*position)
       
    #print(f"Input pos: {position}, Servo Pos  {servo_position} ")
    #servo.init(freq = 50, duty = 512)
    servo.duty_u16(servo_position)
    #time.sleep(.05)
    
    #servoRangeMax=6800
    #servoRangeMin=4700
#     servoZeroservoPosMid=servoRangeMin+int((servoRangeMax-servoRangeMin)/2)
#     normPos=position/-1023.0 # Pos is normalized (from -1.0 to +1.0)
#     
#     servoPos= servoZero + int(((servoRangeMax-servoRangeMin)/2)*normPos)
    position=servoPosMid+position
    if(position<servoPosMin) :
         position=servoPosMin
    if(position>servoPosMax) :
         position=servoPosMax

     #servoPosMid=2500
     #servoPosMax=servoRangeMid+1000
     #servoPosMin=servoRangeMid-1000  #Mid

    #print(normPos,servoPos)
    #servo.duty_u16(position)
    

#valid numbers is from -1024 to +1024
def motorSpeed(speed) :
    #set forward speed
    speedNormalized=speed/1024
    if(speed>0):
        if(speed>1.0):
          speed=1.0
        MotorPinIN1.off()   #off- forward motion 
        MotorSpeed.duty_u16(int(speedNormalized*65535))
    else :
        #MotorSpeed.duty_u16(0)
        MotorPinIN1.on()   #reverse motion
        sp=65535+int(speedNormalized*65535)
        #print(sp)
        MotorSpeed.duty_u16(sp)
        



# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    led.off()
    servo.deinit()
    return 'The server is shutting down...'



class DNSQuery:
	def __init__(self, data):
		self.data = data
		self.domain = ''
		tipo = (data[2] >> 3) & 15  # Opcode bits
		if tipo == 0:  # Standard query
			ini = 12
			lon = data[ini]
			while lon != 0:
				self.domain += data[ini + 1:ini + lon + 1].decode('utf-8') + '.'
				ini += lon + 1
				lon = data[ini]
		#print("searched domain:" + self.domain)

	def response(self, ip):

		#print("Response {} == {}".format(self.domain, ip))
		if self.domain:
			packet = self.data[:2] + b'\x81\x80'
			packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'  # Questions and Answers Counts
			packet += self.data[12:]  # Original Domain Name Question
			packet += b'\xC0\x0C'  # Pointer to domain name
			packet += b'\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
			packet += bytes(map(int, ip.split('.')))  # 4bytes of IP
		#print(packet)
		return packet

# function to handle incoming dns requests
async def run_dns_server():

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set non-blocking otherwise execution will stop at 'recvfrom' until a connection is received
    #  and this will prevent the other async threads from running
    udps.setblocking(False)

    # bind to port 53 on all interfaces
    udps.bind(('0.0.0.0', 53))

    while True:
        try:
            gc.collect()

            data, addr = udps.recvfrom(4096)
            #print("Incoming data...")

            DNS = DNSQuery(data)
            udps.sendto(DNS.response(SERVER_IP), addr)

            #print("Replying: {:s} -> {:s}".format(DNS.domain, SERVER_IP))

            await asyncio.sleep_ms(10)

        except Exception as e:
            #print("Timeout")
            await asyncio.sleep_ms(10000)

    udps.close()


if __name__ == "__main__":
    try:
        #run_dns_server()
        #r=uasyncio.create_task(run_dns_server())
        #app.run(port=80,debug=False)
        loop = asyncio.get_event_loop()
        loop.create_task(run_dns_server())
        loop.create_task(app.run(port=80,debug=False))
        loop.run_forever()
        loop.close()
        
    except KeyboardInterrupt:
        pass

