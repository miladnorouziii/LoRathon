import spidev
import time
import RPi.GPIO as GPIO

class LoRa():

    frequency = 434
    spreadingFactor = 7
    bandWidth = 7
    crcRate = 1
    power = 17
    RFO = False
    preamble = 8
    currentMode = "Receive"
    CRC = True
    syncWord = 56
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)


    #Initial Module with desire states
    def __init__(self, frequency, spreadingFactor, bandWidth, crcRate, power, RFO, crcCheck, syncWord):
        self.frequency = frequency
        self.spreadingFactor = spreadingFactor
        self.bandWidth = bandWidth
        self.crcRate = crcRate
        self.power = power
        self.RFO = RFO
        self.CRC = crcCheck
        self.syncWord = syncWord
        GPIO.output(22, 0)
        time.sleep(.01)
        GPIO.output(22, 1)
        time.sleep(.01)

    #This function write Bytes on spi using spidev driver
    def writeOnSPI(self, address, msg):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 3000000
        spi.xfer2([address | 0x80, msg])
        spi.close()

    def burstWrite(self, address, msg):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 3000000
        spi.xfer2([address | 0x80] + msg)
        spi.close()

    #This function will read bytes from module based on address and desired size
    def readFromSPI(self, address, bytes):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 5000000
        payload = []
        payload.append(address)
        for i in range(bytes):
            payload.append(0xff)
        reply = spi.xfer2(payload)
        spi.close()
        return reply[1:]

    #This function will check if spi can connect to module or not
    def checkConnection(self):
        reply = self.readFromSPI(0x42, 1)
        if reply[0]==0x12:
            return True
        else:
             return False

    def reset(self):
        GPIO.output(22, 0)
        time.sleep(.01)
        GPIO.output(22, 1)
        time.sleep(.01)

    #This Function will change the working Mode
    def workingMode(self, mode):
        reply = self.readFromSPI(0x01, 1)
        if mode=="Sleep":
            data = (reply[0] & 0xF8) | 0x00
            self.currentMode = "Sleep"
        elif mode == "Standby":
            data = (reply[0] & 0xF8) | 0x01
            self.currentMode = "Standby"
        elif mode == "Transmit":
            data = 0x83
            self.currentMode = "Transmit"
        elif mode == "Receive":
            data = 0x85
            self.currentMode = "Receive"
        self.writeOnSPI(0x01, data);

    #This function will set the Spreading factor on module
    def setSF(self, sf):
        reply = self.readFromSPI(0x1E, 1)
        data = (sf << 4) + (reply[0] & 0x0F)
        self.writeOnSPI(0x1E, data);

    def setCrcCheck(self, crcCheck):
        if self.CRC:
            reply = self.readFromSPI(0x1E, 1)
            data = reply[0] | 0x04
            print("trye  data: " + str(data))
            self.writeOnSPI(0x1E, data)
        else:
            reply = self.readFromSPI(0x1E, 1)
            data = reply[0] & 0xfb
            print("false data: " + str(data))
            self.writeOnSPI(0x1E, data)

    def setSync(self, sw):
        self.writeOnSPI(0x39, sw)
        print("Geting data")
        reply = self.readFromSPI(0x39, 1)
        print(str(reply[0]))

#   BW ---------> Input Value
#   7.8KHz ---------> 0
#   10.4KHz ---------> 1
#   15.6KHz ---------> 2
#   20.8KHz ---------> 3
#   31.25KHz ---------> 4
#   41.7KHz ---------> 5
#   62.5KHz ---------> 6
#   125KHz ---------> 7
#   250KHz ---------> 8
#   500KHz ---------> 9

    #This function will change Bandwidth on module. be aware of input value.
    def setBW(self, bandWidth):
        bw = 0
        if bandWidth == 7.8:
            bw = 0
        elif bandWidth == 10.4:
            bw = 1
        elif bandWidth == 15.6:
            bw = 2
        elif bandWidth == 20.8:
            bw = 3
        elif bandWidth == 31.25:
            bw = 4
        elif bandWidth == 41.7:
            bw = 5
        elif bandWidth == 62.5:
            bw = 6
        elif bandWidth == 125:
            bw = 7
        elif bandWidth == 250:
            bw = 8
        elif bandWidth == 500:
            bw = 9
        reply = self.readFromSPI(0x1D, 1)
        data = (bw << 4) + (reply[0] & 0x0F)
        self.writeOnSPI(0x1D, data);

#   CRC ---------> Input Value
#   4/5 ---------> 1
#   4/6 ---------> 2
#   4/7 ---------> 3
#   4/8 ---------> 4

    #This function will change CRC on module
    def setCRC(self, cr):
        crc = 1
        if cr == 5:
            crc = 1
        elif cr == 6:
            crc = 2
        elif cr == 7:
            crc = 3
        elif cr == 8:
            crc = 4
        reply = self.readFromSPI(0x1D, 1)
        data = (reply[0] & 0xF0) + (crc << 1)
        self.writeOnSPI(0x1D, data);

    #This function will set carrier frequency
    def setFREQ(self, fr):
        freq = int(fr * 16384)
        msb = freq >> 16
        mid = (freq & 0xFFFF) >> 8
        lsb = (freq & 0xFF)
        self.writeOnSPI(0x06, msb)
        self.writeOnSPI(0x07, mid)
        self.writeOnSPI(0x08, lsb)

    #This function will set the current protect registers
    def setOCP(self, mA):
        trim = 27
        if mA <= 120:
            trim = (mA - 45) / 5
        elif mA >= 240:
            trim = (mA + 30) / 10
        self.writeOnSPI(0x0B, 0x20 | (0x1F & int(trim)))

    #This function will set output power (PA_Conf is 1)
    def setPWR(self, pwr, RFO):
        if RFO == True:
            if pwr < 0:
                pwr = 0
            elif pwr > 14:
                pwr = 14;
            self.writeOnSPI(0x09, pwr | 0x70)
        else:
            if pwr > 17:
                if pwr > 20:
                    pwr = 20
                pwr = pwr - 3
                self.writeOnSPI(0x4D, 0x87)
                self.setOCP(140)
            else:
                if pwr < 2:
                    pwr = 2
                self.writeOnSPI(0x4D, 0x84)
                self.setOCP(100)
            self.writeOnSPI(0x09, (pwr-2) | 0x80)

    #This function will config the module
    def powerUP(self):
        self.reset()
        self.workingMode("Sleep")
        payload = self.readFromSPI(0x01, 1)
        self.writeOnSPI(0x01, payload[0] | 0x80)
        self.setFREQ(self.frequency)
        self.setPWR(self.power, self.RFO)
        self.writeOnSPI(0x0C, 0x23)                           #This line active maximum gain sensivity
        payload = self.readFromSPI(0x1E, 1)
        #self.writeOnSPI(0x1E, payload[0] | 0x03)              #This line will disable CRC
        self.writeOnSPI(0x1F, 0xFF)                           #Set receiver timeout to maximum (On single Mode)
        self.setSF(self.spreadingFactor)
        self.setCrcCheck(self.CRC)
        self.setBW(self.bandWidth)
        self.setCRC(self.crcRate)
        self.setSync(self.syncWord)
        self.writeOnSPI(0x20, self.preamble >> 8)
        self.writeOnSPI(0x21, self.preamble & 0xFF)
        payload = self.readFromSPI(0x40, 1)
        self.writeOnSPI(0x40, payload[0] | 0x3F)               # Map DIO0 To Receive
        self.workingMode("Standby")
        self.workingMode("Receive")
        if self.checkConnection():
            reply = self.readFromSPI(0x39, 1)
            print("This is ans on 0x39:"+str(reply[0]))
            return True
        else:
            return False

    #This function will check operating registers to check for valid states
    def ping(self):
        if (self.readFromSPI(0x01, 1) != [133]) and self.currentMode == "Receive":
            self.powerUP()


    def transmit(self, msg, timeout):
        length = len(msg)
        self.workingMode("Standby")
        payload = self.readFromSPI(0x0E, 1)
        self.writeOnSPI(0x0D, payload[0])
        self.writeOnSPI(0x22, length)
        self.burstWrite(0x00, msg)
        self.workingMode("Transmit")
        state = True
        while True:
            payload = self.readFromSPI(0x12, 1)
            if((payload[0] & 0x08) != 0):
                self.writeOnSPI(0x12, 0xFF)
                self.workingMode("Receive")
                state = True
                break
            else:
                timeout = timeout - 1
                if timeout == 0:
                    self.workingMode("Receive")
                    state = False
                    break
                time.sleep(0.001)
        return state

    def read(self):
        self.workingMode("Standby")
        payload = self.readFromSPI(0x12, 1)
        message = []
        print("This is payload:"+str(payload[0]))
        if self.CRC:
            if payload[0] & 0x50 == 0x50:
                self.writeOnSPI(0x12, 0xFF)
                bytesLen = self.readFromSPI(0x13, 1)
                payload = self.readFromSPI(0x10, 1)
                self.writeOnSPI(0x0D, payload[0])
                message = self.readFromSPI(0x00, bytesLen[0])
            else:
                print("false CRC")
        else:
            self.writeOnSPI(0x12, 0xFF)
            bytesLen = self.readFromSPI(0x13, 1)
            payload = self.readFromSPI(0x10, 1)
            self.writeOnSPI(0x0D, payload[0])
            message = self.readFromSPI(0x00, bytesLen[0])
        self.writeOnSPI(0x12, 0xFF)
        self.workingMode("Receive")
        return message


#    def pinger(self):
#        while(True):
#            time.sleep(5)
#            print("pinged")
#            self.ping()


#    proc1 = Process(target=pinger)
#    proc1.start()
