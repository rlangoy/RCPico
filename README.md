# Raspbery Pi Pico RC controller
<img src="images/Freecad_gemma_electronics.jpg" width="700">

A car can be controlled using an web-browser on a mobilephone or PC using  WIFI <br>
<img src="images/controller_gui.png" width="200">

The PCB-board is fitted for the 3D printed car [Gamma 2.0](https://cults3d.com/en/3d-model/gadget/gamma-2-demo) <br>
There is no requrement to have the PCB joust connect the hardware compenents using wires show in the [schematics](KicadV7#rp2040-pinout)

<img src="images/RC_No_PCB.jpg" width="350">





## Project Content 

### KicadV7  
PCB Design files for [Kicadv7](https://www.kicad.org/) \
&nbsp; More Hardware info is available in the [README](/KicadV7/README.md) 


# Software
The software is developed using [MicroPython](https://micropython.org/) \
&nbsp;  on a [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) <br>
&nbsp; More Info in the [README](/MicroPython/WifiController/README.md) 

## Instalation
### Firmware 
Download [RCPico.zip](https://github.com/rlangoy/RCPico/releases/download/v1.0/RCPico.zip) <br>

Unzip RCPico.zip <br>
<img src="images/BootSel.png" width="200"> <br>
On the microcontroller, press the BOOTSEL button and hold it while you connect the USB cable to your computer <br>
&nbsp; A new drive would appear <br>
Copy the file RCPico.uf2 to the new drive <br>


## Conneting to the car
Scan the QRcode to connect to the car's wifi-network 

<img src="images/qr_connect_wifi.png" width="200"> 
This conect you to the car-wifi with ssid = 'GemmmaRC#01' and password = '123456789'

Scann the QRcode to connect to the car's controller/joystock

<img src="images/qr_connect_page.png" width="200">
Open the web-page 192.168.4.1 and now you are ready :)

# 3dr Party resources
## Hardware
For a harrdware list see the [Bil of materials](KicadV7#bil-of-materials-bom) :)

## Software compoenents
[microdot - Micropython web framework](https://github.com/miguelgrinberg/microdot) <br>
[nipplejs - JoyStick JavaScript](https://github.com/yoannmoinet/nipplejs)
## Software tools
[picotool](https://github.com/raspberrypi/picotool) used to grenerate the firmware-file (RCPico.u2f)  <br>
&nbsp; (picotool save -a -f RCPPico.uf2) <br>
# License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

