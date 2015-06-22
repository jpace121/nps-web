import spidev

class ADCChip(spidev.SpiDev):
    def __init__(self):
        spidev.SpiDev.__init__(self)
        self.connected = False #Am I connected right now?
        self.cnt = 0 #I'm going to have to reference count the closing of the file...
        self.lock = False # Are communications paused right now?

    def connect(self):
        self.cnt = self.cnt + 1 
        # ^ increment cntr for everyone who tries to connect, thus "claim to
        # access" comes from connection
        # if someone connects multiple times they will mess things up...
        if not self.connected:
            spidev.SpiDev.open(self,1,0)
            self.connected = True

    def close(self):
        if self.connected:
            self.cnt = self.cnt - 1
            if self.cnt == 0:
                spidev.SpiDev.close(self)

    def xfer2(self, in_bytes):
        while True:
            if not self.lock:
                self.lock = True
                out_bytes = spidev.SpiDev.xfer2(self,in_bytes)
                self.lock = False
                break
            else:
                pass

        return out_bytes

        
