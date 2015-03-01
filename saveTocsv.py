import json
import csv
import time
import datetime
import subprocess32 as sub
import glob
import os

# Load config file
with open("/root/python-bluetooth/config.json") as f:
   config_file = json.load(f)
   
ROOT_PATH = str(config_file["rootpath"])

"""
Converts a json file created by the website.py website into a csv file
which can be read in excel.
Module also contains the neccessary OS calls to display and delete the
files from the GUI.
"""

def get_file_list():
   print_list = sub.check_output(["ls",ROOT_PATH + "logs"]).split("\n")
   return print_list

def delete_files():
   to_delete = glob.glob(ROOT_PATH + "logs/*.csv")
   for file in to_delete:
      sub.call(["rm",file])
   to_delete_txt = glob.glob(ROOT_PATH + "logs/*.txt")
   for file in to_delete_txt:
      sub.call(["rm",file])

def zip_for_download():
   print "zip_for_download:"
   ts = time.time()
   filename = datetime.datetime.fromtimestamp(ts).strftime('penetrometer_%Y%m%d_%H%M.zip')
   filepath = "/tmp/"
   orig_dir = sub.check_output(["pwd"]).rstrip()
   os.chdir(ROOT_PATH)
   output = sub.call(["zip","-r","-j",filepath+filename,ROOT_PATH + "logs"])
   os.chdir(orig_dir)
   if output == 0:
      return filepath+filename
   else:
      return False

def makeDataFileName():
    # inspired by http://stackoverflow.com/questions/13890935/timestamp-python
   ts = time.time()
   filename = datetime.datetime.fromtimestamp(ts).strftime('penetrometer_%Y%m%d_%H%M%S.csv')
   filepath = ROOT_PATH + "logs/" #use environment variable?
   return filepath+filename

def get_file(filename):
    return ROOT_PATH + "logs/" + filename 

def jsonToCSV(str_file, filename = False):
   # Step 1, remove a layer of nodes.
   big_dict = {}
   json_file = json.loads(str_file)
   for first_key in json_file.keys():
      # Try catch else block tries to fix error that occurs when hannset data is None. An alternative approach would be an if is None style approach as per below
      try:
         json_file[first_key].keys()
      except AttributeError:
	 big_dict[first_key] = json_file[first_key]
      else:
         for second_key in json_file[first_key].keys():
            big_dict[first_key+"_"+second_key] = json_file[first_key][second_key]
         
   # Step 2: What is the max number of iterations needed to loop through the longest list?
   max_len = 0
   for key in big_dict.keys():
      # if not is None check to catch error when distance_sesor returns no values.
      if not big_dict[key] is None and len(big_dict[key]) > max_len:
         max_len = len(big_dict[key])

   if not filename:
      filename = makeDataFileName()
   else:
      filename = ROOT_PATH + "logs/" + filename

   with open(filename,'w') as csv_file:
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
            except TypeError:
               elem = " "
            row.append(elem)
         writer.writerow(row)
         
def CSVtoDict(csv_file):
   """Translates a CSV file to dictionary for use later. Assume that csv_file
   has been opened elsewhere, and will be closed there as well.
   I'm also assuming the structure of the CSV here, unlike what I did in the
   previous function, where everything is generic."""
   # TODO: Make this function generic.
   data_dict = {'range_vals':{'t':[],'d':[]},'donut_vals':{'t':[],'d':[]},'cone_vals':{'t':[],'d':[]}}
   fieldnames = ("range_vals_t","range_vals_d","donut_vals_t","donut_vals_d","cone_vals_t", "cone_vals_d")
   dictreader = csv.DictReader(csv_file,fieldnames)
   for line in dictreader:
      data_dict['range_vals']['t'].append(line['range_vals_t'])
      data_dict['range_vals']['d'].append(line['range_vals_d'])
      data_dict['donut_vals']['t'].append(line['donut_vals_t'])
      data_dict['donut_vals']['d'].append(line['donut_vals_d'])
      data_dict['cone_vals']['t'].append(line['cone_vals_t'])
      data_dict['cone_vals']['d'].append(line['cone_vals_d'])

   # Might want to delete empty elements in here somewhere?
   return data_dict

if __name__ == "__main__":
   get_file_list()
   print(zip_for_download())
   with open('./test.json','r') as f:
      test_json = f.read()
      filename = makeDataFileName()
      print filename
      jsonToCSV(test_json)
   with open(filename,'r') as f:
      CSVtoJSON(f)
   delete_files()
