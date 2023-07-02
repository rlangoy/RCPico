from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket

#from microdot_wsgi import Microdot, send_file
#from microdot_websocket import with_websocket

#from microdot import Microdot, send_file
#from microdot_websocket import with_websocket


#from microdot_asyncio_websocket import websocket
import time
import network
wlan = network.WLAN(network.STA_IF) # create station interface
print(wlan.ifconfig()  )
# Initialize MicroDot
app = Microdot()
#Response.default_content_type = 'text/html'


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
    while True:
        data = await ws.receive()
        if(type(data) is str) :
            print('Received data from client: {} - type is: {}'.format(data, type(data)))
            data = '{}_{}'.format(data, 'ack')
            await ws.send(data)

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == "__main__":
    try:
        app.run(port=80,debug=True)
    except KeyboardInterrupt:
        pass
