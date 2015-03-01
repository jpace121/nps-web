import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from StringIO import StringIO
import json

# Open config file
with open("/root/python-bluetooth/config.json") as f:
    config_file = json.load(f)

def makePlot(input, style='sensors'):
    # Styles:
    #    1. sensors = the style used by sensor.html
    #    2. hump = the style used by analysis.html
    # This is a way to catch for when the data does not exist. It is slightly
    # convoluted.
    data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}, 'donut_vals':{"t":[],"d":[]}}
    # need something like unwrap_or, instead of this nonsense.
    try:
        data["range_vals"]["t"] = input["range_vals"]["t"]
    except (KeyError, TypeError):
        data["range_vals"]["t"] = []
    try:
        data["range_vals"]["d"] = input["range_vals"]["d"]
    except (KeyError, TypeError):
        data["range_vals"]["d"] = []
    try:
        data["cone_vals"]["t"] = input["cone_vals"]["t"]
    except (KeyError, TypeError):
        data["cone_vals"]["t"] = []
    try:
        data["cone_vals"]["d"] = input["cone_vals"]["d"]
    except (KeyError, TypeError):
        data["cone_vals"]["d"] = []
    try:
        data["donut_vals"]["t"] = input["donut_vals"]["t"]
    except (KeyError, TypeError):
        data["donut_vals"]["t"] = []
    try:
        data["donut_vals"]["d"] = input["donut_vals"]["d"]
    except (KeyError, TypeError):
        data["donut_vals"]["d"] = []

    # Actual Plotting Here
    plt.clf() # clear figure
    plt.figure(1) # optional
    if style == 'sensors':
        axis1 = plt.subplot(2, 1, 1) # just like matlab...
        try:
            plt.plot(data["range_vals"]["t"],data["range_vals"]["d"],'r.-')
        except ValueError:
            plt.plot(0,0)
        plt.ylabel('Distance (in)') #this will be a pressure by the time it gets here
        plt.xlabel('Time (s)')
        plt.legend(['Range Values'], 'lower right')

    if style == 'hump':
        axis2 = plt.subplot(1,1,1)
    else:
        axis2 = plt.subplot(2, 1, 2, sharex=axis1)
    try:
        plt.plot(data["cone_vals"]["t"],data["cone_vals"]["d"],'b.-')
        plt.plot(data["donut_vals"]["t"],data["donut_vals"]["d"],'g.-')
    except ValueError:
        plt.plot(0,0)
    plt.ylabel('Voltage (V)') #this will be a pressure by the time it gets here
    plt.xlabel('Time (s)')
    if style == 'hump':
        lgd = plt.legend(["Cone Values", "Donut Values"], 'upper right')
    else:
        lgd = plt.legend(["Cone Values", "Donut Values"], 'lower right')
    
    # from http://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask
    img = StringIO()
    plt.savefig(img, bbox_inches="tight") # for production
    
    if config_file["save_tmp_plot"]:
        plt.savefig('/tmp/test.png') # for debug only
    img.seek(0)
    return img

if __name__ == '__main__':
    data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}, 'donut_vals':{"t":[],"d":[]}}
    #data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}}
    data["range_vals"]["t"] = [0,1,2,3]
    data["range_vals"]["d"] = [0,1,2,3]
    data["cone_vals"]["t"] = [0,1,2,3,4,5]
    data["cone_vals"]["d"] = [0,1,4,9,15,25]
    data["donut_vals"]["t"] = [0,1,2,3,4,5]
    data["donut_vals"]["d"] = [0,1,8,27,64,125]
    makePlot(data)
