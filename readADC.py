import spidev
from time import sleep

V_ref = 4.93# I need a more constant reference voltage...

def pull_once(chan_set=1):
    """Measure the differential voltage once. At channel "chan_set".
         - chan_set 1 => Ch0+ Ch1-
         - chan_set 2 => Ch2+ Ch3-
    """
    global V_ref
    spi = spidev.SpiDev()
    spi.open(1,0)
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

if __name__ == "__main__":
    for i in range(0,10):
        print pull_once(2)
        sleep(0.5)
