from __future__ import print_function
import sys
import spidev
from time import sleep
import threading

V_ref = 4.93# I need a more constant reference voltage...

class ForceSensor(object):
    def __init__(self,chan_select):
        self.chan_select = chan_select # 1 for 0-1, 2 for 2-3
        if(self.chan_select == 1):
            # 0-1
            self.cal_m = 0
            self.cal_b = 0
        elif(self.chan_select == 2):
            # 2-3
            self.cal_m = 0
            self.cal_b = 0
        else:
            # throw error
            print("forceSensor.py: Invalid channel selection.",file=sys.err)
        self.thread = None
        self.streaming = False
        self.lock = False
        self.spi = None
        self.connected = False # instead of this, just check for truthiness of self.spi?

    def connect(self):
        if not self.connected:
            self.connected = True
            self.spi = spidev.SpiDev()
            self.spi.open(1,0)

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
        if self.streaming:
            self.streaming = False
            data = self.thread.stop()
            self.lock = False
            values = [_v_to_lbs(self.cal_m,self.cal_b,x) for x in data]
        else:
            values = None
        return values

    def __del__(self):
        if(self.connected):
            self.spi.close()
        
def _read_once(chan_set,spi):
    """Measure the differential voltage once. At channel "chan_set".
         - chan_set 1 => Ch0+ Ch1-
         - chan_set 2 => Ch2+ Ch3-
    """
    global V_ref
    # What channel do you want?
    if chan_set == 1:
        to_send = [ 0b00000100,0b00000000,0]
    elif chan_set == 2:
        to_send = [ 0b00000100,0b10000000,0]
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
        self.data = []

    def run(self):
        """run is the function ran by the thread"""
        while(not self.stop_event.is_set()):
            # read values until stop is sent
            response = _read_once(self.chan_select,self.spi)
            #print(response)
            self.data.append(response) # Push response to the data list for later
            sleep(0.0001) # I should be bigger....
        return

    def stop(self):
        """When called, stops the while loop in the thread"""
        self.stop_event.set()
        return self.data
        
if __name__ == "__main__":
    sensor = ForceSensor(1)
    sensor.connect()
    sensor.streamStart()
    sleep(0.1)
    sensor.streamStop()
        
