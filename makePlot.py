import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def makePlot(data):
    # I should calculate frcition ratios in here.
    plt.plot(data["range_vals"]["t"],data["range_vals"]["d"],'r--',
             data["cone_vals"]["t"],data["cone_vals"]["d"],'b--',
             data["donut_vals"]["t"],data["donut_vals"]["d"],'g--')
    plt.ylabel('Voltage (V)') #this will be a pressure by the time it gets here
    plt.xlabel('Time (s)')
    plt.legend(['Range Values', 'Cone Values', 'Donut Values'],'upper right')
    plt.savefig('/tmp/temp.png')
    return '/tmp/temp.png'

if __name__ == '__main__':
    data = {'range_vals':{"t":[],"d":[]},'cone_vals': {"t":[],"d":[]}, 'donut_vals':{"t":[],"d":[]}}
    data["range_vals"]["t"] = [0,1,2,3]
    data["range_vals"]["d"] = [0,1,2,3]
    data["cone_vals"]["t"] = [0,1,2,3]
    data["cone_vals"]["d"] = [0,1,4,9]
    data["donut_vals"]["t"] = [0,1,2,3]
    data["donut_vals"]["d"] = [0,1,8,27]
    makePlot(data)
