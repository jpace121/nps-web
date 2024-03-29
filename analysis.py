from saveTocsv import CSVtoDict
import saveTocsv as saveCSV
from findpeaks import detect_peaks
import sys
import numpy as np
import json
import makePlot as plot
import base64

with open('/root/python-bluetooth/config.json') as f:
    config_file = json.load(f)

def find_maxes(filename):
    """
       Find peaks and related post processing for log files.
       Assumes that 'filename' is a valid file at rootpath/logs.
    """
    file = open(config_file['rootpath']+'/logs/'+filename)
    data = CSVtoDict(file)
    file.close()

    # "Unpack" the CSV
    cone_vals_t = np.array(data['cone_vals']['t'])
    cone_vals_t = np.delete(cone_vals_t, 0, 0) # delete first line (the header)
    cone_vals_t = cone_vals_t[cone_vals_t != " "]  # remove empty elements
    cone_vals_t = cone_vals_t.astype('float')  # convert to floats
    
    donut_vals_t = np.array(data['donut_vals']['t'])
    donut_vals_t = np.delete(donut_vals_t, 0, 0)
    donut_vals_t = donut_vals_t[donut_vals_t != " "] 
    donut_vals_t = donut_vals_t.astype('float')
    
    range_vals_t = np.array(data['range_vals']['t'])
    range_vals_t = np.delete(range_vals_t, 0, 0)
    range_vals_t = range_vals_t[range_vals_t != " "]
    range_vals_t = range_vals_t.astype('float')
    
    cone_vals_d = np.array(data['cone_vals']['d'])
    cone_vals_d = np.delete(cone_vals_d, 0, 0)
    cone_vals_d = cone_vals_d[cone_vals_d != " "]
    cone_vals_d = cone_vals_d.astype('float')
    
    donut_vals_d = np.array(data['donut_vals']['d'])
    donut_vals_d = np.delete(donut_vals_d, 0, 0)
    donut_vals_d = donut_vals_d[donut_vals_d != " "]
    donut_vals_d = donut_vals_d.astype('float')
    
    range_vals_d = np.array(data['range_vals']['d'])
    range_vals_d = np.delete(range_vals_d, 0, 0)
    range_vals_d = range_vals_d[range_vals_d != " "]
    range_vals_d = range_vals_d.astype('float')
    
    # Find max positions.
    # (Most of the following was taken from my analyze_one script.)
    donut_freq = 1/np.mean(np.diff(donut_vals_t))
    cone_freq = 1/np.mean(np.diff(cone_vals_t))

    max_loc_cone = detect_peaks(cone_vals_d, mpd = np.floor(0.5*cone_freq),
                                mph = 0.5) # 0.5 is around the zero line
    max_loc_donut = detect_peaks(donut_vals_d, mpd = np.floor(0.5*donut_freq),
                                 mph = 0.1) # 0.1 is around the zero line

    # Crop accordingly.
    # for each max, pull the 0.1s around them.
    # 0.1s is an approximation, and may be way off base. We will need to play with it.
    # for ease of use, Im going to use the cone peaks as the "true" peaks.
    # I also have to include the range
    crop_width = 0.05/2
    cone_cropped = [] 
    donut_cropped = []
    range_cropped = []
    max_cone_cropped = []
    max_donut_cropped = []
    max_range_cropped = []
    max_indice_donut = -1
    for max_indice in max_loc_cone:
        max_indice_donut = max_indice_donut + 1 # also need to increment through donut_locs
        
        nStart = max_indice - (0.2*crop_width)*cone_freq # not integers...
        nEnd = max_indice + (0.8*crop_width)*cone_freq # not integers...

        if nStart < 0:
            nStart = 0
        if nEnd > len(cone_vals_t):
            nEnd = len(cone_vals_t) - 1
        
        cone_cropped.append((cone_vals_t[nStart:nEnd],cone_vals_d[nStart:nEnd]))
        donut_cropped.append((donut_vals_t[nStart:nEnd],donut_vals_d[nStart:nEnd]))
        
        max_cone_cropped.append(cone_vals_d[max_indice])
        max_donut_cropped.append(donut_vals_d[max_indice_donut])

        range_index_max = _findnearest(range_vals_t, cone_vals_t[max_indice]) + 1
        max_range_cropped.append(range_vals_d[range_index_max]-range_vals_d[0])
        
        range_nStart = _findnearest(range_vals_t, cone_vals_t[nStart]) - 5
        range_nEnd = _findnearest(range_vals_t, cone_vals_t[nEnd]) + 6
        
        if range_nStart < 0:
            range_nStart = 0
        if range_nEnd > len(range_vals_t):
            range_nEnd = len(range_vals_t)
        range_cropped.append((range_vals_t[range_nStart:range_nEnd],donut_vals_d[range_nStart:range_nEnd]))

    # For each range of points, plot the stuff.
    plot_dict = []
    for cone_set, donut_set, range_set in zip(cone_cropped, donut_cropped, range_cropped):
        # Save values to CSV and save filename ot dict
        big_dict = {"range_vals":{"t":range_set[0].tolist(), "d":range_set[1].tolist()},
                    "cone_vals":{"t":cone_set[0].tolist(), "d":cone_set[1].tolist()},
                    "donut_vals":{"t":donut_set[0].tolist(), "d":donut_set[1].tolist()}}
        # Make plot and save in dict
        img = plot.makePlot(big_dict, style='hump')
        plot_dict.append(base64.b64encode(img.getvalue()))

        # Find depth for which


    return (plot_dict, max_cone_cropped, max_donut_cropped, max_range_cropped)

def calc_frict_ratio(cone_maxes, donut_maxes, range_maxes, filename):
    """Calculate friction ratios, given arrays of cone_maxes and donut_maxes,
       the corresponding depths, and the filename with the timestamp it
       should be saved under.
       Save data as a file and return values. """
    # Areas to calculate the friction ratios.
    A_cone = config_file["areas"]["cone"]
    A_donut = config_file["areas"]["donut"]
    
    # Convert voltages to pressure (V -> psi)
    cone_max_f = []
    for cone_max in cone_maxes:
        lb = config_file['calibValues']['cone_m']*cone_max + \
             config_file['calibValues']['cone_b']
        psi = lb/A_cone
        cone_max_f.append(psi)
        
    donut_max_f = []
    for donut_max in donut_maxes:
        lb = config_file['calibValues']['donut_m']*donut_max + \
             config_file['calibValues']['donut_b']
        psi = lb/A_donut
        donut_max_f.append(psi)
    
    # Calculate friction ratio.
    friction_ratios = []
    for i in range(0, len(cone_max_f)):
        Fr = (donut_max_f[i]/cone_max_f[i])*100
        friction_ratios.append(Fr)

    # Convert cone max f to bar
    cone_max_bar = []
    for elem in cone_max_f:
        cone_max_bar.append(elem*0.0689476)

    with open(_makefilename(filename), 'w') as f:
        f.write('depth (in), fri (%), qc (bar) \n')
        for i in range(0,len(friction_ratios)):
            f.write(str(range_maxes[i]) + ',' + str(friction_ratios[i]) + ',' + str(cone_max_bar[i]) + '\n')

    return (friction_ratios, cone_max_bar)
    
def _findnearest(array,value):
    """Find the index of numpy array 'array' which is nearest to 'value'. """
    return (np.abs(array-value)).argmin()

def _makefilename(filename):
    return config_file["rootpath"] + '/logs/' + filename.split('/')[-1].split(".")[0] + "_analyzed.txt"

    
if __name__ == "__main__":
    print find_maxes(sys.argv[1])
