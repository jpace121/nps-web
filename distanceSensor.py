from __future__ import print_function
import sys
import serial
from time import sleep #because flush is non blocking?

class DistanceSensor(object):
    def __init__(self, fileAddr):
        # Open the serial port for the sensor
        self.connected = False
        try:
            self.serial = serial.Serial(fileAddr, 9600)
        except serial.serialutil.SerialException:
           print("distanceSensor.py: Could not connect to serial port.", file=sys.stderr)
        else:
            self.connected = True


    def getDistance(self):

        # send "read" signal
        self.serial.flush()
        self.serial.write('g\r\n')

        # read the signal until \n
        response = self.serial.readline() # reads until EOL
       
        # Check for errors.
        # If there is an error, return None and log. If ok, return val.
        
        if response[0] == "@":
            print("distanceSensor.py: Error Received from handset", file=sys.stderr)
            val = None
        elif len(response) != 34:
            print("distanceSensor.py: Response from hanset not expected number of bytes", file=sys.stderr)
            val = None
        elif response[0:7] != "31..02+":
            print("distanceSensor.py: Response Violate initial value assumption", file=sys.stderr)
            val = None
        else:
            # Parse out the actual distance from the noise
            val = int(response[7:15])/10.
            
        return val

    def isAlive(self):
        # Send command
        self.serial.flush()
        self.serial.write('a\r\n')
        # Read repsonse, looking for '?'
        val = self.serial.readline()

        if(val == '?\r\n'):
            return True
        else:
            return False

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/tty.DISTOD3910350799-Serial')
    if mySensor.connected:
        assert(mySensor.isAlive())
        print(mySensor.getDistance())
        assert(mySensor.isAlive())
