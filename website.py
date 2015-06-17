from distanceSensor import DistanceSensor
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from time import sleep

app = Flask(__name__)
app.config['DEBUG'] = True # should be False in production

# Sensor related gloabl variables
range_finder = DistanceSensor('/dev/cu.usbmodem1421')
#range_finder = DistanceSensor('/dev/tty.DISTOD3910350799-Serial')

@app.route('/')
@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/sensors.html')
def sensors_html():
    return render_template('sensors.html')

@app.route('/_get_range_vals') #I may want to make this a post instead of get?
def get_range_values_get():
    global range_finder
    option = request.args.get('option','None')
    if option == "stream_start":
        while True:
            if range_finder.isAlive():
                range_finder.streamStart()
                response = "stream_started"
                break
            else:
                sleep(1) #0.25 is kind of fast, no one is in hurry...
    elif option == "stream_stop":
        response = range_finder.streamStop()
    elif option == "once":
        while True:
            if range_finder.isAlive():
                response = {}
                response['range'] = range_finder.getDistance()
                break
            else:
                sleep(1)
    elif option == "connect":
        if not range_finder.connected:
            range_finder.connect()
            response = "connected"
        if not range_finder.connected:
            response = "error"
    elif option == "disconnect":
        if range_finder.connected:
            range_finder.disconnect()
            response = "disconnected"
        if range_finder.connected:
            response = "error"
    else:
        response = "error"
    return jsonify(result=response)

@app.route('/downloads.html')
def downloads_html():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run()

