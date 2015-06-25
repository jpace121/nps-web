import json
import csv
from pprint import pprint # for testing
import time
import datetime
import numpy as np

"""
Converts a json file created by the website.py website into a csv file
which can be read in excel.
"""

def makeDataFileName():
    # inspired by http://stackoverflow.com/questions/13890935/timestamp-python
   ts = time.time()
   return datetime.datetime.fromtimestamp(ts).strftime('penetrometer_%Y%m%d_%H%M%S.csv')

def jsonToCSV(json_file):
   # this is nonoptimal and prbably overly slow...
   # it's also ugly...
   # Step 1, remove a layer of nodes.
   big_dict = {}
   for first_key in json_file.keys():
      for second_key in json_file[first_key].keys():
         big_dict[first_key+"_"+second_key] = json_file[first_key][second_key]
         
   # Step 2: Write header
   
   np.savetxt(makeDataFileName(),big_dict)

if __name__ == "__main__":
    with open('./test.json','r') as f:
        test_json = json.load(f)
        print makeDataFileName()
        jsonToCSV(test_json)
