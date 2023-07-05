
/*
  Joystick code from:
  https://github.com/yoannmoinet/nipplejs
*/

let  ack=true;

let  strPendingWebSocketMesage=""  // The last message not sendt due to quing

var connection = new WebSocket('ws://'+location.host+'/ws');

connection.onopen = function () {
  //  connection.send('Connect ' + new Date());
  //  connection.send("I123"); // Send Msg to recieve GUI update

    //Debugonnection.send(rgbstr);
    //document.getElementById("Slider1TextVal").style = "background-color:lightgreen";
};

connection.onerror = function (error) {
    console.log('WebSocket Error ', error);
};

connection.onmessage = function (e) {  
    //console.log('Server: ', e.data);
    ack=true;
    // If message was qued send it...
    if(strPendingWebSocketMesage !=="")
       { connection.send(strPendingWebSocketMesage); 
         strPendingWebSocketMesage=""
        }
};

connection.onclose = function(){
    console.log('WebSocket connection closed');
    //Debug
    //document.getElementById("Slider1TextVal").style = "background-color:red";
};



var radius = 100;
var sampleJoystick = {
    zone: document.getElementById('joystick_base'), 
    mode: 'static',
    position: {
      left: '50%',
      top:   '175px' //'10%'
    },
    size: radius*2,
    color: 'black'
};

var joystick;
var position;
joystick = nipplejs.create(sampleJoystick);


joystick.on('start end', function(evt, data)
 {
  position = data; }).on('move', function(evt, data) {
  position = data;
  
  // <--> Send data as web-sockets
  //console.log('On Move', data.distance, 'rad', data.angle.radian);
  var xSpeed= data.distance*Math.cos(data.angle.radian)/100.0;
  var ySpeed= data.distance*Math.sin(data.angle.radian)/100.0;

  //console.log('X:', xSpeed, 'Y: ', ySpeed);
  ySpeed=ySpeed*1024;
  xSpeed=xSpeed*1024;
  if(ack==true) {
   
     const jsonData = { "xPos":  Math.round(xSpeed) , "yPos" : Math.round(ySpeed) };
     const jsonSrting= JSON.stringify(jsonData);
     connection.send(jsonSrting);
     ack=false;
   }
   else
   {   //there is a que to send messages update the que-header
       // All other messages is droped...
       const qJsonData = { "xPos":  Math.round(xSpeed) , "yPos" : Math.round(ySpeed) };
       const qJsonSrting= JSON.stringify(qJsonData);

       //console.log('quing ', qJsonSrting);
       strPendingWebSocketMesage=qJsonSrting
   }
   
  
 // motor1=

}).on('end',
      function(evt, data) {        
  
  const xjsonData = { "xPos":  000 , "yPos" : 000 };
  const xJsonSrting= JSON.stringify(xjsonData);
  connection.send(xJsonSrting);
  strPendingWebSocketMesage= ""   //Clear message Buff
 // console.log('on end -joy released');
}
     ).on('pressure', function(evt, data) {
  position=data;
  //console.log('on pressure');

});
