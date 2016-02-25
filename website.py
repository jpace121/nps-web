from __future__ import print_function
from distanceSensor import DistanceSensor
from forceSensor import ForceSensor
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, send_file
from werkzeug import secure_filename
from time import sleep, time
import saveTocsv as tocsv
import json
import makePlot as plot
from nocache import nocache
import analysis
import thread

app = Flask(__name__)
app.config['DEBUG'] = True # should be False in production

# Sensor related global variables
connect_time = time()
#range_finder = DistanceSensor('/dev/cu.usbmodem1421')
range_finder = DistanceSensor('/dev/rfcomm0', connect_time)
force_sensor = ForceSensor(connect_time)

# Global variable to maintain the state of the app.
# Neccessary so on page reloads can be grabbed by js.
# This is only used for maintaining the GUI, does not effect the operation 
# of the application.
app_status = {"connected":False, "streaming":False}

# ugly global variable for the figure to be plotted.
fig = "  "

# config for file uploads
app.config['UPLOAD_FOLDER'] = './uploads' # for testing
#app.config['UPLOAD_FOLDER'] = '/root/python-bluetooth/uploads' # for realz

# Guarantees the uploaded file is a valid file type
def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['csv']

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
    global force_sensor
    global fig
    global app_status
    option = request.args.get('option','None')
    if option == "stream_start":
        if not range_finder.streaming:
            while not range_finder.isAlive():
                sleep(0.1)
        if not range_finder.streaming:
            range_finder.streamStart()
        if not force_sensor.streaming:
            force_sensor.streamStart()
        if not range_finder.streaming or not force_sensor.streaming:
            response = "error"
        else:
            response = "stream_started"
            app_status["streaming"] = True
    elif option == "stream_stop":
        data = {}
        data['range_vals'] = range_finder.streamStop()
        (data['cone_vals'], data['donut_vals']) = force_sensor.streamStop()
        if app_status["streaming"]: #only update fig if I was streaming
            fig = plot.makePlot(data)
        jsoned = json.dumps(data)
        thread.start_new_thread(tocsv.jsonToCSV, (jsoned,))
        response = "stream_stop"
        app_status["streaming"] = False
    elif option == "once":
        response = {}
        response['range'] = None
        (response['cone_force'], response['donut_force']) = force_sensor.getForce()
        while True:
            if range_finder.isAlive():
                response['range'] = range_finder.getDistance()
                break
            else:
                sleep(0.1)
    elif option == "connect":
        if not range_finder.connected:
            range_finder.connect()
        if not force_sensor.connected:
            force_sensor.connect()
        if range_finder.connected and force_sensor.connected:
            response = "connected"
            app_status["connected"] = True
        else:
            response = "error"
    elif option == "disconnect":
        if range_finder.connected:
            range_finder.disconnect()
        if force_sensor.connected:
            force_sensor.disconnect()
        if not range_finder.connected and not force_sensor.connected:
            response = "disconnected"
            app_status["connected"] = False
        else:
            response = "error"
    elif option == "get_status":
        response = app_status
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

# For downloading the zip file...
@app.route('/log_files')
def _get_file():
    return send_file(tocsv.zip_for_download(), as_attachment=True)

@app.route('/log/<filename>')
def log_get(filename):
    return send_file(tocsv.get_file(filename), as_attachment=True)

@app.route('/image/fig')
@nocache
def fig_fn():
    return send_file(fig, mimetype='image/png')
    
@app.route('/analysis.html')
def analysis_html():
    return render_template('analysis.html')

@app.route('/_analysis/upload', methods = ['POST'])
def _analysis_upload():
    file = request.files['file']
    if file and allowed_filename(file.filename):
        (filename_dict, plot_dict) = analysis.analysis(file, file.filename)
        response = {'filenames':filename_dict,'plots':plot_dict}
    else:
        response = "error"
    return jsonify(result = response)
        
if __name__ == '__main__':
    app.run()
