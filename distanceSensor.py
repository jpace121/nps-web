from __future__ import print_function
import sys
import serial
from time import sleep #because flush is non blocking?
import time
import threading
from Queue import Queue

def valid_response(response):
    """Given a repsonse from the handset, detemrine if valid."""
    val = False
    # Check for errors.
    # If there is an error, return False.
    if response is None:
        # This check was added after server started.
	print("distanceSensor.py: Handset repsonse is None.")
    elif len(response) == 0:
        print("distanceSensor.py: Handset sent a stringof length zero.")
    elif response[0] == "@":
        print("distanceSensor.py: Error Received from handset", file=sys.stderr)
    elif len(response) != 34:
        print("distanceSensor.py: Response from handset not expected number of bytes", file=sys.stderr)
    elif response[0:7] != "31..02+":
        print("distanceSensor.py: Response Violate initial value assumption", file=sys.stderr)
    else:
        # Parse out the actual distance from the noise
        val = True
    return val
    
def interp_response(response):
    """Interprets a VALID repsonse."""
    return (int(response[7:15])/10.)
    
class _ThreadRead_(threading.Thread):
    """Reads values from distance sensor in its streaming mode in
       a separate thread."""
    def __init__(self,serial):
        threading.Thread.__init__(self)
        self.serial = serial
        self.stop_event = threading.Event()
        self.data = {"t": [ ], "d": [ ]}

    def run(self):
        """run is the function ran by the thread"""
        # Ask for streaming values 
        self.serial.flush()
        self.serial.write('h\r\n')
        
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response = self.serial.readline() # reads until EOL
            self.data["t"].append(time.time())
            self.data["d"].append(response) # Push response to the data list for later
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
        self.streaming = False
        self.lock = False
        self.connect_time = None

    def connect(self):
        """Does the connection."""
        if not self.connected:
            try:
                self.serial = serial.Serial(self.fileAddr, 9600, timeout=5)
            except serial.serialutil.SerialException:
                print("distanceSensor.py: Could not connect to serial port.", file=sys.stderr)
            else:
                self.connected = True
                self.connect_time = time.time()
        else:
            pass

    def disconnect(self):
        if self.connected:
            self.serial.close()
            self.connected = False
            
    def getDistance(self):
        # send "read" signal
        if not self.lock:
            self.lock = True
            self.serial.flush()
            self.serial.write('g\r\n')

            # read the signal until \n
            resp = self.serial.readline() # reads until EOL
            self.lock = False

            # Return the interpreted response (need a better none)
            return (interp_response(resp) if valid_response(resp) else None)
        else:
            return None

    def isAlive(self):
        """Tells if hanset is reponsive. Call before calling any other
           method. It is the only method that checks..."""
        resp = None
        if(self.lock):
            # If I'm locked I was alive before, and we can assume I'm still alive.
            resp = True
        if(self.connected and not self.lock):
            # Send command
            self.lock = True
            self.serial.flush()
            self.serial.write('a\r\n')
            # Read repsonse, looking for '?'
            val = self.serial.readline()
            self.lock = False

            if(val == '?\r\n'):
                resp = True
        return resp

    def streamStart(self):
        """Puts handset in streaming mode and pulls the values in a
           separate thread.
           The values are returned from streamstop"""
        if (not self.streaming and not self.lock):
            self.lock = True
            self.thread = _ThreadRead_(self.serial)
            self.thread.start()
            self.streaming = True

    def streamStop(self):
        """Stops the streaming and returns the values from it."""
        values = {"t": [], "d": []}
        bigTime = []
        if self.streaming:
            self.streaming = False
            data = self.thread.stop()
            self.serial.write('t\r\n') # tell the handset to stop sending
            self.lock = False
            for i in range(0, len(data["d"])):
                if valid_response(data["d"][i]):
                    values["d"].append(interp_response(data["d"][i]))
                    bigTime.append(data["t"][i])
            values["t"] = [x - self.connect_time for x in bigTime] #convert epoch times to reasonable times
            #values = [interp_response(x) for x in data if valid_response(x)] # RIP magical one liner
        else:
            values = None
        return values

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/rfcomm0')
    #mySensor = DistanceSensor('/dev/tty.DISTOD3910350799-Serial')
    mySensor.connect()
    #sleep(2) # Arduino is stupid
    while True:
        if mySensor.isAlive():
            print(mySensor.getDistance())
            mySensor.streamStart()
            sleep(2)
            print(mySensor.streamStop())
            break
        else:
            sleep(0.25)
