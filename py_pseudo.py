import serial

class DistanceSensor(object):
    def __init__(self,fileAddr ):
        # Open the serial port for the sensor
        self.serial = serial.Serial(fileAddr, 9600) # this guy can be private


    def getDistance(self):
        NUMBYTESRESPONSE = 15
        NUMSTARTGOODBYTE = 7

        # send "read" signal
        self.serial.flush();
        self.serial.write('g\n')

        # read the signal until \n
        response = self.serial.readline() # reads until EOL
        self.serial.flush()
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
            #err = "Error Received"
            val = None
        elif len(response) != 34:
            #err = "Too small"
            val = None
        elif response[0:7] != "31..02+":
            #err = "Violate initial value assumption"
            val = None
        else:
            # Parse out the actual distance from the noise
            val = int(response[NUMSTARTGOODBYTE:NUMBYTESRESPONSE])/10.
            
        return val

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/tty.DISTOD3910350799-Serial');
    val = mySensor.getDistance()
    print val
