import serial

class DistanceSensor(object):
    def __init__(self,fileAddr ):
        # Open the serial port for the sensor
        self.serial = serial.Serial(fileAddr, 9600) # this guy can be private


    def getDistance(self):
        NUMBYTESRESPONSE = 15
        NUMSTARTGOODBYTE = 7
        # send read signal
        self.serial.flush();
        self.serial.write('g\n')
       
        # read the response
        #self.serial.read(34) #reads all the bytes
        #response = self.serial.read(NUMBYTESRESPONSE) # reads only the first "relevant" number ignoring the "EOL" number
        
        response = self.serial.readline() # reads until EOL
        self.serial.flush()
        print response
        
        # Check for error. (I miss match statements. This could also be implemented as a dict, but that translates crappily to Java, so I won't.)
        if response[0] == "@":
            print "Error Received"
        elif len(response) != 34:
            print "Too small"
        elif response[0:7] != "31..02+":
            print "Violate initial value assumption"
        else:
            # Parse out the actual distance from the noise
            val = int(response[NUMSTARTGOODBYTE:NUMBYTESRESPONSE])/10.
            #print response[NUMSTARTGOODBYTE:NUMBYTESRESPONSE]
            return val

if __name__ == '__main__':
    mySensor = DistanceSensor('/dev/tty.DISTOD3910350799-Serial');
    print mySensor.getDistance()
