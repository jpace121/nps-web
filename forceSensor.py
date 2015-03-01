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
    """This object represents both force sensors."""
    def __init__(self,connect_time):
        # 0-1
        self.cal_m_1 = 0
        self.cal_b_1 = 0
        # 6-7
        self.cal_m_2 = 0
        self.cal_b_2 = 0
        
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
            measured_voltage1 = _read_once(1,self.spi)
            measured_voltage2 = _read_once(2,self.spi)
            force1 = _v_to_lbs(self.cal_m_1,self.cal_b_1,measured_voltage1)
            force2 = _v_to_lbs(self.cal_m_2,self.cal_b_2,measured_voltage2)
        else:
            force1 = None
            force2 = None
            print("forceSensor.py: getForce, spi not connected.",file=sys.stderr)
        return (force1, force2)

    def streamStart(self):
        if (not self.streaming and not self.lock and self.connected):
            self.lock = True
            self.thread = _ThreadRead_(self.spi)
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
            values1["d"] = [_v_to_lbs(self.cal_m_1,self.cal_b_1,x) for x in data1["d"]]
            values2["d"] = [_v_to_lbs(self.cal_m_2,self.cal_b_2,x) for x in data2["d"]]
        else:
            values1 = None
            values2 = None
        return (values1, values2)

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
    def __init__(self,spi):
        threading.Thread.__init__(self)
        self.spi = spi
        self.stop_event = threading.Event()
        self.data1 = {"t": [], "d": []}
        self.data2 = {"t": [], "d": []}

    def run(self):
        """run is the function ran by the thread"""
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response1 = _read_once(1,self.spi)
            response2 = _read_once(2,self.spi)
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
    sensor = ForceSensor(time.time())
    sensor.connect()
    print(sensor.getForce())
    #sensor.streamStart()
    #sleep(0.00000000001)
    #print("Sample Freq:")
    #(sensor1, sensor2) = sensor.streamStop()
    #print(sensor1["d"])
    #print(sensor2["d"])
    
