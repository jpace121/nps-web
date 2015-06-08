from distanceSensor import DistanceSensor
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from time import sleep

app = Flask(__name__)
app.config['DEBUG'] = True # should be False in production

# Sensor related gloabl variables
#range_finder = DistanceSensor('/dev/cu.usbmodem1421')
range_finder = DistanceSensor('/dev/tty.DISTOD3910350799-Serial')

@app.route('/')
@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/receive', methods=['POST','GET'])
def receive():
    pass;
"""
    number1 = request.form['number1']
    number2 =request.form['number2']
    summed = int(number1) + int(number2)
    return render_template('receive.html',sum=summed)
"""
@app.route('/range_finder.html')
def range_finder_html():
    global range_finder
    range_finder.connect()
    return render_template('range_finder.html')

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
                response = range_finder.getDistance()
                break
            else:
                sleep(1)
    else:
        response = "error"
    return jsonify(result=response)

if __name__ == '__main__':
    app.run()

