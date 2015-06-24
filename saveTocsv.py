import json
import csv
from pprint import pprint # for testing
import time
import datetime

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
   with open("./logs/" + makeDataFileName(),"w") as csv_file:
        csv_writer = csv.writer(csv_file)
        # write first row
        head_row = []
        for first_key in json_file.keys():
            for second_key in json_file[first_key].keys():
                head_row.append(first_key + "_" + second_key)
        csv_writer.writerow(head_row)
        # Make sure each column is the same lenght, where data is not
        # write a " " char.
        lens = {}
        for first_key in json_file.keys():
           for second_key in json_file[first_key].keys():
              lens[first_key+","+second_key] = len(json_file[first_key][second_key])
        for key in lens.keys(): 
            if lens[key] < max(lens.values()):
               
               
         

if __name__ == "__main__":
    with open('./test.json','r') as f:
        test_json = json.load(f)
        print makeDataFileName()
        jsonToCSV(test_json)
