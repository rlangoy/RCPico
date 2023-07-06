# WIFI Remote Controller
<img src="/images/controller_gui.png" width="200">
Place the finger on the dot to controll the car :)

## Installation

Install Micropython and copy all the files from /MicroPython/WifiController to the device..

### Conneting to the car
Scan the QRcode to connect to the car's wifi-network 

<img src="/images/qr_connect_wifi.png" width="200"> 
This conect you to the car-wifi with ssid = 'GemmmaRC#01' and password = '123456789'

Scann the QRcode to connect to the car's controller/joystock

<img src="/images/qr_connect_page.png" width="200">
Open the web-page 192.168.4.1 and now you are ready :)


## Details
The Server side is buildt around two parts:
### Basic file server
  Uses [microdot (a web framework)](https://github.com/miguelgrinberg/microdot) to provide web-client files located in the ./static folder. <br>
  The root request ( / ) forwards the ./static/index.html pages that locads the userinterface as show in the picture below  
  <img src="/images/controller_gui.png" width="200">
### Remote Control
  The [joystick (nipplejs)](https://github.com/yoannmoinet/nipplejs) in the web-client reads the position from the controller and forwards to the microcontroller as a
  WebSocket("ws://192.168.1.4/ws") message  where the positionis formated as a [JSON](https://json.org/) string.<br>
  &nbsp; WebScoket Remote control format :
  &nbsp;&nbsp; { "xPos":  xxx , "yPos" : yyy }  <br> 
  &nbsp;&nbsp;&nbsp;&nbsp; xxx - is an integer from -1024 to 1024 ( turning left / right ) <br>
  &nbsp;&nbsp;&nbsp;&nbsp; yyy - is an integer from -1024 to 1024 ( motor speed ) <br>
   

