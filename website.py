from __future__ import print_function
from distanceSensor import DistanceSensor
from forceSensor import ForceSensor
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, send_file
from time import sleep, time
import saveTocsv as tocsv
import json
import makePlot as plot
from nocache import nocache
import thread

app = Flask(__name__)
app.config['DEBUG'] = True # should be False in production

# Sensor related gloabl variables
connect_time = time()
#range_finder = DistanceSensor('/dev/cu.usbmodem1421')
range_finder = DistanceSensor('/dev/rfcomm0', connect_time)
cone_sensor = ForceSensor(1, connect_time)
donut_sensor = ForceSensor(2, connect_time)

# ugly global variable for the figure to be plotted.
fig = "  "

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
    global cone_sensor
    global donut_sensor
    global fig
    option = request.args.get('option','None')
    if option == "stream_start":
        if not range_finder.streaming:
            while not range_finder.isAlive():
                sleep(1)
        if not range_finder.streaming:
            range_finder.streamStart()
        if not donut_sensor.streaming:
            donut_sensor.streamStart()
        if not cone_sensor.streaming:
            cone_sensor.streamStart()
        if not range_finder.streaming or not donut_sensor.streaming or not cone_sensor.streaming:
            response = "error"
        else:
            response = "stream_started"
    elif option == "stream_stop":
        data = {}
        data['range_vals'] = range_finder.streamStop()
        data['cone_vals'] = cone_sensor.streamStop()
        data['donut_vals'] = donut_sensor.streamStop()
        fig = plot.makePlot(data)
        jsoned = json.dumps(data)
        thread.start_new_thread(tocsv.jsonToCSV, (jsoned,))
        response = "stream_stop"
    elif option == "once":
        response = {}
        response['range'] = None
        response['cone_force'] = cone_sensor.getForce()
        response['donut_force'] = donut_sensor.getForce()
        while True:
            if range_finder.isAlive():
                response['range'] = range_finder.getDistance()
                break
            else:
                sleep(1)
    elif option == "connect":
        if not range_finder.connected:
            range_finder.connect()
        if not donut_sensor.connected and not cone_sensor.connected:
            donut_sensor.connect()
            cone_sensor.connect()
        if range_finder.connected and cone_sensor.connected and donut_sensor.connected:
            response = "connected"
        else:
            response = "error"
    elif option == "disconnect":
        if range_finder.connected:
            range_finder.disconnect()
        if donut_sensor.connected:
            donut_sensor.disconnect()
        if cone_sensor.connected:
            cone_sensor.disconnect()
        if not cone_sensor.connected and not cone_sensor.connected and not donut_sensor.connected:
            response = "disconnected"
        else:
            response = "error"
    else:
        response = "error"
    return jsonify(result=response)

@app.route('/downloads.html')
def downloads_html():
    return render_template('downloads.html')

@app.route('/_get_downloads')
def _get_dowloads_html():
    option = request.args.get('option','None')
    if option == "update":
        response = tocsv.get_file_list()
    elif option == "delete":
        tocsv.delete_files()
        response = "delete"
    else:
        response = "error"
    return jsonify(result=response)

@app.route('/log_files')
def _get_file():
    return send_file(tocsv.zip_for_download())

@app.route('/image/fig')
@nocache
def fig_fn():
    return send_file(fig, mimetype='image/png')
    
    
if __name__ == '__main__':
    app.run()

