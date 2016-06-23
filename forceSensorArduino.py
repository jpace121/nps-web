"""
forceSensorArduino replaces the SPI controlled ADC on the beaglebone with a
Arduino, talking to the computer over Serial.

This is very slow. Approximately 60 Hz max, which is not even close to 5.8 kHz
we were looking for.
"""

from __future__ import print_function
import sys
from time import sleep
import time
import threading
import serial

V_ref = 5.# I need a more constant reference voltage...

class ForceSensor(object):
    """This object represents both force sensors."""
    def __init__(self,fileAddr,connect_time):
        self.thread = None
        self.fileAddr = fileAddr
        self.streaming = False
        self.lock = False
        self.serial = None
        self.connected = False # instead of this, just check for truthiness of self.spi?
        self.connect_time = connect_time

    def connect(self):
        if not self.connected:
            try:
                self.serial = serial.Serial(self.fileAddr, 9600)
                sleep(1) # Arduino is stupid
            except serial.serialutil.SerialException:
                print("forceSensorArduino.py: Could not connect to serial port.", file=sys.stderr)
            else:
                self.connected = True
        else:
            pass
            
    def disconnect(self):
        if self.connected:
            self.serial.close()
            self.connected = False

    def getForce(self):
        """Gets a force once."""
        if self.connected:
            if not self.lock:
                self.lock = True
                measured_voltage1 = _read_once(1,self.serial)
                measured_voltage2 = _read_once(2,self.serial)
                self.lock = False
            else:
                print("forceSensorArduino.py: getForce, already locked.")
                measured_voltage1 = None
                measured_voltage2 = None
        else:
            measured_voltage1 = None
            measured_voltage2 = None
            print("forceSensorArduino.py: getForce, serial not connected.",file=sys.stderr)
        return (measured_voltage1, measured_voltage2)

    def streamStart(self):
        if (not self.streaming and not self.lock and self.connected):
            self.lock = True
            self.thread = _ThreadRead_(self.serial)
            self.thread.start()
            self.streaming = True

    def streamStop(self):
        values1 = {"t": [], "d": []}
        values2 = {"t": [], "d": []}
        if self.streaming:
            self.streaming = False
            (data1, data2) = self.thread.stop()
            self.lock = False
            values1["t"] = [x - self.connect_time for x in data1["t"]]
            values2["t"] = [x - self.connect_time for x in data2["t"]]
            values1["d"] = [x for x in data1["d"]]
            values2["d"] = [x for x in data2["d"]]
        else:
            values1 = None
            values2 = None
        return (values1, values2)

    def __del__(self):
        if(self.connected):
            self.serial.close()
        
def _read_once(chan_set,serial):
    """Measure the differential voltage once. At channel "chan_set".
         - chan_set 1 => Ch0+ Ch1-
         - chan_set 2 => Ch6+ Ch7-
    """
    global V_ref
    # What channel do you want?
    if chan_set == 1:
        #serial.flush()
        serial.write('b')
        dig_response_code = serial.readline()
    elif chan_set == 2:
        #serial.flush()
        serial.write('d')
        dig_response_code = serial.readline()
    else:
        # Hey, an unneccessary error check!
        pass # aka do nothing

    dig_response_code.strip() # remove whitespace
    dig_response_code = int(dig_response_code)
    
    V_in = float(dig_response_code*V_ref)/4096
    return V_in

def _v_to_lbs(slope,offset,V):
    """Converts a reading from the ADC to a lb force.
       Long term, I'm doing this in the analysis functions."""
    return V # without slope and offset data, keep this a stub

class _ThreadRead_(threading.Thread):
    """Reads values from sensor in its streaming mode in
       a separate thread."""
    def __init__(self,serial):
        threading.Thread.__init__(self)
        self.serial = serial
        self.stop_event = threading.Event()
        self.data1 = {"t": [], "d": []}
        self.data2 = {"t": [], "d": []}

    def run(self):
        """run is the function ran by the thread"""
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response1 = _read_once(1,self.serial)
            response2 = _read_once(2,self.serial)
            #print(response)
            self.data1["d"].append(response1) # Push response to the data list for later
            self.data2["d"].append(response2) # Push response to the data list for later
            curTime = time.time()
            self.data1["t"].append(curTime)
            self.data2["t"].append(curTime)
            #sleep(0.0001) # I need to be small enough to capture peaks.
        return

    def stop(self):
        """When called, stops the while loop in the thread"""
        self.stop_event.set()
        return (self.data1, self.data2)

if __name__ == "__main__":
    sensor = ForceSensor('/dev/tty.usbmodem1421',time.time())
    sensor.connect()
    #print(sensor.getForce())
    sensor.streamStart()
    sleep(1)
    print("Sample Freq:")
    (sensor1, sensor2) = sensor.streamStop()
    #print(sensor1["d"])
    #print(sensor2["d"])
    print(len(sensor1["d"]))
    
