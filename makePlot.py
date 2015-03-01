import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from StringIO import StringIO

def makePlot(input):
    # I should calculate frcition ratios in here.
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

    plt.clf() # clear figure
    plt.plot(data["range_vals"]["t"],data["range_vals"]["d"],'r--',
             data["cone_vals"]["t"],data["cone_vals"]["d"],'b--',
             data["donut_vals"]["t"],data["donut_vals"]["d"],'g--')
    plt.ylabel('Voltage (V)') #this will be a pressure by the time it gets here
    plt.xlabel('Time (s)')
    plt.legend(['Range Values', 'Cone Values', 'Donut Values'],'lower right')
    # from http://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask
    img = StringIO()
    plt.savefig(img)
    img.seek(0)
    return img

if __name__ == '__main__':
    data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}, 'donut_vals':{"t":[],"d":[]}}
    #data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}}
    data["range_vals"]["t"] = [0,1,2,3]
    data["range_vals"]["d"] = [0,1,2,3]
    data["cone_vals"]["t"] = [0,1,2,3]
    data["cone_vals"]["d"] = [0,1,4,9]
    data["donut_vals"]["t"] = [0,1,2,3]
    data["donut_vals"]["d"] = [0,1,8,27]
    print makePlot(data)
