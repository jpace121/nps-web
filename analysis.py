from saveTocsv import CSVtoDict
from findpeaks import detect_peaks
import sys
import numpy as np
import json

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
    cone_vals_t = cone_vals_t.astype('float')  # convert to floats
    
    donut_vals_t = np.array(data['donut_vals']['t'])
    donut_vals_t = np.delete(donut_vals_t, 0, 0)
    donut_vals_t = donut_vals_t.astype('float')
    
    range_vals_t = np.array(data['range_vals']['t'])
    range_vals_t = np.delete(range_vals_t, 0, 0)
    range_vals_t = range_vals_t.astype('float')
    
    cone_vals_d = np.array(data['cone_vals']['d'])
    cone_vals_d = np.delete(cone_vals_d, 0, 0)
    cone_vals_d = cone_vals_d.astype('float')
    
    donut_vals_d = np.array(data['donut_vals']['d'])
    donut_vals_d = np.delete(donut_vals_d, 0, 0)
    donut_vals_d = donut_vals_d.astype('float')
    
    range_vals_d = np.array(data['range_vals']['d'])
    range_vals_d = np.delete(range_vals_d, 0, 0)
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
    crop_width = 0.1/2
    cone_cropped = [] 
    donut_cropped = []
    range_cropped = []
    for max_indice in max_loc_cone:
        nStart = max_indice - crop_width*cone_freq
        nEnd = max_indice + crop_width*cone_freq
        
        cone_cropped.append((cone_vals_t[nStart,nEnd],cone_vals_d[nStart,nEnd]))
        donut_cropped.append((donut_vals_t[nStart,nEnd],donut_vals_d[nStart,nEnd]))
        
        range_nStart = _findnearest(range_vals_t, cone_vals_t[nStart]) - 1
        range_nEnd = _findnearest(range_vals_t, cone_vals_t[nEnd]) + 1
        range_cropped.append((range_vals_t[range_nStart,range_nEnd],donut_vals_d[range_nStart,range_nEnd]))

    # For each group:
    # 1. Save values into CSV, save filename in dict.
    # 2. Plot graph, save the resulting StringIO to dict.
    # fin
    # jsonify result, send to client.
    n = 1 # 1 not 0, zero will freak out jsonToCSV
    for cone_set, donut_set, range_set in zip(cone_cropped, donut_cropped, range_cropped):
        big_dict = {"range_vals":{"t":range_cropped[0], "d":range_cropped[1]},
                    "cone_vals":{"t":cone_cropped[0], "d":cone_cropped[1]},
                    "donut_vals":{"t":donut_cropped[0], "d":donut_cropped[1]}}
        filenameset = _makefilename(filename, n)
        n = n + 1
        CSVtoDict.jsonToCSV(json.dumps(big_dict),filename = filenameset)
        


def _findnearest(array,value):
    """Find the index of numpy array 'array' which is nearest to 'value'. """
    return (np.abs(array-value)).argmin()

def _makefilename(filename, n):
    return filename.split(".")[0] + "_[" + str(n) + "].csv"

    
if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        print analysis(f,sys.argv[1])
