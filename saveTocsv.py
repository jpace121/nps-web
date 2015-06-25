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
   filename = datetime.datetime.fromtimestamp(ts).strftime('penetrometer_%Y%m%d_%H%M%S.csv')
   filepath = "./logs/"
   return filepath+filename

def jsonToCSV(json_file):
   # this is nonoptimal and prbably overly slow...
   # it's also ugly...
   # Step 1, remove a layer of nodes.
   big_dict = {}
   for first_key in json_file.keys():
      for second_key in json_file[first_key].keys():
         big_dict[first_key+"_"+second_key] = json_file[first_key][second_key]
         
   # Step 2: What is the max number of iterations needed to loop through the longest list?
   max_len = 0
   for key in big_dict.keys():
      if len(big_dict[key]) > max_len:
         max_len = len(big_dict[key])

   with open(makeDataFileName(),'w') as csv_file:
      writer = csv.writer(csv_file)
      # Step 3: Write first row.
      writer.writerow(sorted(big_dict.keys(),reverse=True))
      # Step 4: Loop through that number of times. If the value is missing, put a " ".
      for i in range(0,max_len):
         row = []
         for key in sorted(big_dict.keys(),reverse=True):
            try:
               elem = big_dict[key][i]
            except IndexError:
               elem = " "
            row.append(elem)
         writer.writerow(row)

if __name__ == "__main__":
    with open('./test.json','r') as f:
        test_json = json.load(f)
        print makeDataFileName()
        jsonToCSV(test_json)
