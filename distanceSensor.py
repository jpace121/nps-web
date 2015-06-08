from __future__ import print_function
import sys
import serial
from time import sleep #because flush is non blocking?
import threading
from Queue import Queue

def interp_response(response):
    """Given a repsonse from the handset, transforms it into a number."""
    # Check for errors.
    # If there is an error, return None and log. If ok, return val.
    if response[0] == "@":
        print("distanceSensor.py: Error Received from handset", file=sys.stderr)
        val = None
    elif len(response) != 17: # this was 34 for some reason pre-Arduino?
        print("distanceSensor.py: Response from handset not expected number of bytes", file=sys.stderr)
        val = None
    elif response[0:7] != "31..02+":
        print("distanceSensor.py: Response Violate initial value assumption", file=sys.stderr)
        val = None
    else:
        # Parse out the actual distance from the noise
        val = int(response[7:15])/10.
    return val
    
class _ThreadRead_(threading.Thread):
    """Reads values from distance sensor in its streaming mode in
       a separate thread."""
    def __init__(self,serial):
        threading.Thread.__init__(self)
        self.serial = serial
        self.stop_event = threading.Event()
        self.data = []

    def run(self):
        """run is the function ran by the thread"""
        # Ask for streaming values 
        self.serial.flush()
        self.serial.write('h\r\n')
        
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response = self.serial.readline() # reads until EOL
            self.data.append(response) # Push response to the data list for later
        return

    def stop(self):
        """When called, stops the while loop in the thread"""
        self.stop_event.set()
        return self.data

class DistanceSensor(object):
    def __init__(self, fileAddr):
        # Open the serial port for the sensor
        self.connected = False
        self.fileAddr = fileAddr
        self.serial = None

    def connect(self):
        """Does the connection."""
        if not self.connected:
            try:
                self.serial = serial.Serial(self.fileAddr, 9600, timeout=3)
            except serial.serialutil.SerialException:
                print("distanceSensor.py: Could not connect to serial port.", file=sys.stderr)
            else:
                self.connected = True
        else:
            pass
            
    def getDistance(self):
        # send "read" signal
        self.serial.flush()
        self.serial.write('g\r\n')

        # read the signal until \n
        response = self.serial.readline() # reads until EOL

        # Return the interpreted response
        return interp_response(response)

    def isAlive(self):
        """Tells if hanset is reponsive. Call before calling any other
           method. It is the only method that checks..."""
        resp = False
        if(self.connected):
            # Send command
            self.serial.flush()
            self.serial.write('a\r\n')
            # Read repsonse, looking for '?'
            val = self.serial.readline()

            if(val == '?\r\n'):
                resp = True
        return resp

    def streamStart(self):
        """Puts handset in streaming mode and pulls the values in a
           separate thread.
           The values are returned from streamstop"""
        self.thread = _ThreadRead_(self.serial)
        self.thread.start()

    def streamStop(self):
        """Stops the streaming and returns the values from it."""
        values = []
        data = self.thread.stop()
        self.serial.write('t\r\n') # tell the handset to stop sending
        for response in data:
            values.append(interp_response(response))
        return values

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/cu.usbmodem1421')
    mySensor.connect()
    #sleep(2) # Arduino is stupid
    while True:
        if mySensor.isAlive():
            print(mySensor.getDistance())
            mySensor.streamStart()
            sleep(11)
            print(mySensor.streamStop())
            break
        else:
            sleep(0.5)
