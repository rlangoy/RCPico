from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from machine import Pin,PWM
import json

import time
import network
wlan = network.WLAN(network.STA_IF) # create station interface
print(wlan.ifconfig()  )
# Initialize MicroDot
app = Microdot()
#Response.default_content_type = 'text/html'
### Motor
MotorPinIN1=Pin(14,Pin.OUT)
MotorPinIN2=Pin(15,Pin.OUT)
MotorPinIN1.off()   #off- forward on -Backword

MotorSpeed=PWM(Pin(15,Pin.OUT))
MotorSpeed.freq(20)
MotorSpeed.duty_u16(00000)

##
servo=PWM(Pin(13))
servo.freq(50)

servoRangeMax=6800
servoRangeMin=4700
servoZero=servoRangeMin+int((servoRangeMax-servoRangeMin)/2)
servo.duty_u16(servoZero)


led = machine.Pin("LED", machine.Pin.OUT)
led.off()                 # set pin to "on" (high) level


# root route
@app.get('/')
def index(request):
    return send_file('/static/index.html')



#The socket needs flow-control if not the input buffer wil be flooded
#The web-client must wait for reply before sending more data
@app.route('/ws')
@with_websocket
async def ws(request, ws):
    c = 0
    led.on()
    servo.duty_u16(servoZero)               # set pin to "on" (high) level
    while True:
        data = await ws.receive()
        if(type(data) is str) :
            #print('Received data from client: {} - type is: {}'.format(data, type(data)))
            jsonRecievedData=json.loads(data)
            xPos=jsonRecievedData['xPos']    # Get the xPos element fro the JSON dataobj
            yPos=jsonRecievedData['yPos']    # Get the xPos element fro the JSON dataobj
            
            if(type(xPos) is int) :         #check if data is a int (recieved properly)                   
               print(f"xPos {xPos}") # Debug data
               turnWheel(xPos)        #Move steering-wheels

            if(type(yPos) is int) :         #check if data is a int (recieved properly)                   
               print(f"yPos {yPos}") # Debug data
               motorSpeed(yPos)
               
            data = '{}_{}'.format(data, 'ack')        # Echo response
            await ws.send(data)          # send ack to recieve more data

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)

#Turn the car to the left/right
#valid numbers is from -1024 to +1024
def turnWheel(position) :
    #servoRangeMax=6800
    #servoRangeMin=4700
    servoZero=servoRangeMin+int((servoRangeMax-servoRangeMin)/2)
    normPos=position/-1023.0 # Pos is normalized (from -1.0 to +1.0)
    servoPos= servoZero + int(((servoRangeMax-servoRangeMin)/2)*normPos)
    if(servoPos<servoRangeMin) :
        servoPos=servoRangeMin
    if(servoPos>servoRangeMax) :
        servoPos=servoRangeMax
    
    servo.duty_u16(servoPos)

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


if __name__ == "__main__":
    try:
        app.run(port=80,debug=True)
    except KeyboardInterrupt:
        pass

