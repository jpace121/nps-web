from __future__ import print_function
import sys
from time import sleep
import time
import threading
from ADCChip import ADCChip

V_ref = 5.# I need a more constant reference voltage...
the_chip = ADCChip() # there is only one chip, so only one spi connection

# Using Ch0 and Ch1 for one sensor and Ch6 and Ch7 for the other one
# (on the ADC). Ch 2 and Ch3 do not seem to diff. This may be a programming
# thing or it may be my wiring, or it may be the ADC is bad....

class ForceSensor(object):
    """This object represents a single force sensor. """
    def __init__(self,chan_select,connect_time):
        self.chan_select = chan_select # 1 for 0-1, 2 for 6-7
        if(self.chan_select == 1):
            # 0-1
            self.cal_m = 0
            self.cal_b = 0
        elif(self.chan_select == 2):
            # 6-7
            self.cal_m = 0
            self.cal_b = 0
        else:
            # throw error
            print("forceSensor.py: Invalid channel selection.",file=sys.err)
        self.thread = None
        self.streaming = False
        self.lock = False
        self.spi = the_chip
        self.connected = False # instead of this, just check for truthiness of self.spi?
        self.connect_time = connect_time

    def connect(self):
        if not self.connected:
            self.connected = True
            self.connect_time = time.time()
            self.spi.connect()

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.spi.close()

    def getForce(self):
        """Gets a force once."""
        if self.connected:
            measured_voltage = _read_once(self.chan_select,self.spi)
            force = _v_to_lbs(self.cal_m,self.cal_b,measured_voltage)
        else:
            force = None
            print("forceSensor.py: getForce, spi not connected.",file=sys.stderr)
        return force

    def streamStart(self):
        if (not self.streaming and not self.lock and self.connected):
            self.lock = True
            self.thread = _ThreadRead_(self.chan_select,self.spi)
            self.thread.start()
            self.streaming = True

    def streamStop(self):
        values = {"t": [], "d": []}
        if self.streaming:
            self.streaming = False
            data = self.thread.stop()
            self.lock = False
            values["t"] = [x - self.connect_time for x in data["t"]]
            values["d"] = [_v_to_lbs(self.cal_m,self.cal_b,x) for x in data["d"]]
        else:
            values = None
        return values

    def __del__(self):
        if(self.connected):
            self.spi.close()
        
def _read_once(chan_set,spi):
    """Measure the differential voltage once. At channel "chan_set".
         - chan_set 1 => Ch0+ Ch1-
         - chan_set 2 => Ch6+ Ch7-
    """
    global V_ref
    # What channel do you want?
    if chan_set == 1:
        to_send = [ 0b00000100,0b00000000,0]
    elif chan_set == 2:
        to_send = [ 0b00000101,0b10000000,0]
    else:
        # Hey, an unneccessary error check!
        to_send = [0,0,0] # aka do nothing

    # Send values.
    response = spi.xfer2(to_send)
    # Translates response (from Senior Design Team 23 Code)
    dig_response_code = (response[1] << 8) & 0b111100000000
    dig_response_code = dig_response_code | (response[2] & 0xff)
    
    V_in = float(dig_response_code*V_ref)/4096
    return V_in

def _v_to_lbs(slope,offset,V):
    """Converts a reading from the ADC to a lb force."""
    return V # without slope and offset data, keep this a stub

class _ThreadRead_(threading.Thread):
    """Reads values from sensor in its streaming mode in
       a separate thread."""
    def __init__(self,chan_select,spi):
        threading.Thread.__init__(self)
        self.chan_select = chan_select
        self.spi = spi
        self.stop_event = threading.Event()
        self.data = {"t": [], "d": []}

    def run(self):
        """run is the function ran by the thread"""
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response = _read_once(self.chan_select,self.spi)
            #print(response)
            self.data["d"].append(response) # Push response to the data list for later
            self.data["t"].append(time.time())
            sleep(0.01) # I should be bigger....
        return

    def stop(self):
        """When called, stops the while loop in the thread"""
        self.stop_event.set()
        return self.data
        
if __name__ == "__main__":
    sensor1 = ForceSensor(1,time.time())
    sensor2 = ForceSensor(2,time.time())
    sensor1.connect()
    sensor2.connect()
    print(sensor2.getForce())
    sensor1.streamStart()
    sensor2.streamStart()
    sleep(0.5)
    print(sensor1.streamStop())
    print(sensor2.streamStop())
    sensor1.disconnect()
    print(the_chip.cnt)
    sensor1.streamStart()
    sensor2.streamStart()
    sensor1.streamStart()
    sensor2.streamStart()
    sleep(0.5)
    print(sensor1.streamStop())
    print(sensor2.streamStop())
