from saveTocsv import CSVtoDict
import saveTocsv as saveCSV
from findpeaks import detect_peaks
import sys
import numpy as np
import json
import makePlot as plot
import base64

# What do we need to do?
# Read the data in from computer [x] 
# Translate to a pythonic object [x]
# Find peaks [x]
# Clip data around peaks. [x]
# Save csv of clipped data [ ]
# Gaph clipped data. [ ]
# Send graphs and filenames via json to frontend [ ]

def analysis(file,filename):
    """
       Perform all of the post processing for files.
       (Is it smart to do all of this in one function?)
       Assumes file is an already open csv file, and it is someone elses job
       to close it.
    """
    data = CSVtoDict(file)

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
    for max_indice in max_loc_cone:
        nStart = max_indice - (0.2*crop_width)*cone_freq # not integers...
        nEnd = max_indice + (0.8*crop_width)*cone_freq # not integers...
        
        cone_cropped.append((cone_vals_t[nStart:nEnd],cone_vals_d[nStart:nEnd]))
        donut_cropped.append((donut_vals_t[nStart:nEnd],donut_vals_d[nStart:nEnd]))
        
        range_nStart = _findnearest(range_vals_t, cone_vals_t[nStart]) - 5
        range_nEnd = _findnearest(range_vals_t, cone_vals_t[nEnd]) + 6
        range_cropped.append((range_vals_t[range_nStart:range_nEnd],donut_vals_d[range_nStart:range_nEnd]))

    # For each group:
    # jsonify result, send to client.
    filename_dict = []
    plot_dict = []
    n = 1
    for cone_set, donut_set, range_set in zip(cone_cropped, donut_cropped, range_cropped):
        # Save values to CSV and save filename ot dict
        big_dict = {"range_vals":{"t":range_set[0].tolist(), "d":range_set[1].tolist()},
                    "cone_vals":{"t":cone_set[0].tolist(), "d":cone_set[1].tolist()},
                    "donut_vals":{"t":donut_set[0].tolist(), "d":donut_set[1].tolist()}}
        filenameset = _makefilename(filename, n)
        filename_dict.append(filenameset)
        n = n + 1
        saveCSV.jsonToCSV(json.dumps(big_dict),filename = filenameset)
        # Make plot and save in dict
        img = plot.makePlot(big_dict, style='hump')
        plot_dict.append(base64.b64encode(img.getvalue()))

    return (filename_dict, plot_dict)
    
def _findnearest(array,value):
    """Find the index of numpy array 'array' which is nearest to 'value'. """
    return (np.abs(array-value)).argmin()

def _makefilename(filename, n):
    return filename.split('/')[-1].split(".")[0] + "_[" + str(n) + "].csv"

    
if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        print analysis(f,sys.argv[1])
