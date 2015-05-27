import serial
from time import sleep #because flush is non blocking

class DistanceSensor(object):
    def __init__(self,fileAddr ):
        # Open the serial port for the sensor
        # In Java, may move to separate build method, which is not the
        # constructor, which should allow us to cath errors better.
        self.connected = False
        try:
            self.serial = serial.Serial(fileAddr, 9600) # can be private
        except serial.serialutil.SerialException:
            print "Can not find serial port."
        else:
            self.connected = True


    def getDistance(self):
        NUMBYTESRESPONSE = 15
        NUMSTARTGOODBYTE = 7

        # send "read" signal
        self.serial.flush()
        self.serial.write('g\r\n')

        # read the signal until \n
        response = self.serial.readline() # reads until EOL
        #print repr(response)
        #print response
        
        # Check for errors.
        # If there is an error, return 0.0 for val and set err to an error
        # string. If no error set err to None and val to the value in inches.
        # This needs to be translated to idiomatic Java.

        # If there is an error, return None, (NaN in Java). If ok, return
        # val. This will be expensive in Java b/c I will have to use Float 
        # instead of float, but I don't think performance is that critical 
        # for this...
        if response[0] == "@":
            print "Error Received"
            val = None
        elif len(response) != 34:
            print "Too small"
            val = None
        elif response[0:7] != "31..02+":
            print "Violate initial value assumption"
            val = None
        else:
            # Parse out the actual distance from the noise
            val = int(response[NUMSTARTGOODBYTE:NUMBYTESRESPONSE])/10.
            
        return val

    def isAlive(self):
        # Send command
        self.serial.flush()
        self.serial.write('a\r\n')
        # Read repsonse, looking for '?'
        val = self.serial.readline()
        #val = self.serial.read(1) # does not work
        #print repr(val)
        if(val == '?\r\n'):
            return True
        else:
            print "a repsonse: " + repr(val)
            return False

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/tty.DISTOD3910350799-Serial');
    if mySensor.connected:
        assert(mySensor.isAlive())
        print mySensor.getDistance()
        assert(mySensor.isAlive())
