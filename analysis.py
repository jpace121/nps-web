from saveTocsv import CSVtoDict
import sys

if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        print CSVtoDict(f)
