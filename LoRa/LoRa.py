import spidev
import time
import RPi.GPIO as GPIO
from .Const import *

class LoRa():

    frequency = 434
    spreadingFactor = 7
    bandWidth = 7
    crcRate = 1
    power = 17
    RFO = False
    preamble = 8
    currentMode = "ReceiveCON"
    CRC = True
    syncWord = 56
    rstPin = 22
    GPIO.setmode(GPIO.BCM)
    
    #Initial Module with desire states
    def __init__(self, rstPin, frequency, spreadingFactor, bandWidth, crcRate, power, RFO, crcCheck, syncWord):
        self.frequency = frequency
        self.spreadingFactor = spreadingFactor
        self.bandWidth = bandWidth
        self.crcRate = crcRate
        self.power = power
        self.RFO = RFO
        self.CRC = crcCheck
        self.syncWord = syncWord
        self.rstPin = rstPin
        GPIO.setup(rstPin, GPIO.OUT)
        GPIO.output(rstPin, 0)
        time.sleep(.01)
        GPIO.output(rstPin, 1)
        time.sleep(.01)

    #This function write Bytes on spi using spidev driver
    def writeOnSPI(self, address, msg):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 3000000
        spi.xfer2([address | 0x80, msg])
        spi.close()

    #This function write Bytes on spi using spidev driver
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

    #This function will change working mode
    def changeWorkingMode(self, mode):
        reply = self.readFromSPI(REG.REG_OP_MODE, 1)
        if mode == "Sleep":
            data = MODES.MODE_LONG_RANGE_MODE | MODES.MODE_SLEEP
            self.currentMode = "Sleep"
        elif mode == "Standby":
            data = MODES.MODE_LONG_RANGE_MODE | MODES.MODE_STDBY
            self.currentMode = "Standby"
        elif mode == "Transmit":
            data = MODES.MODE_LONG_RANGE_MODE | MODES.MODE_TX
            self.currentMode = "Transmit"
        elif mode == "ReceiveCON":
            data = MODES.MODE_LONG_RANGE_MODE | MODES.MODE_RX_CONTINUOUS
            self.currentMode = "ReceiveCON"
        elif mode == "ReceiveSIN":
            data = MODES.MODE_LONG_RANGE_MODE | MODES.MODE_RX_SINGLE
            self.currentMode = "ReceiveSIN"
        self.writeOnSPI(REG.REG_OP_MODE, data)

    #This function will check if spi can connect to module or not
    def checkConnection(self):
        reply = self.readFromSPI(REG.REG_VERSION, 1)
        if reply[0]==0x12:
            return True
        else:
             return False

    #This function will reset module
    def reset(self):
        GPIO.output(self.rstPin, 0)
        time.sleep(.01)
        GPIO.output(self.rstPin, 1)
        time.sleep(.01)

    #This function will set the Spreading factor on module
    def setSpreadingFactor(self, sf):
        if sf < 6:
            sf = 6
        elif sf > 12:
            sf = 12
        if sf == 6:
            self.writeOnSPI(REG.REG_DETECTION_OPTIMIZE, 0xC5)
            self.writeOnSPI(REG.REG_DETECTION_THRESHOLD, 0x0C)
        else:
            self.writeOnSPI(REG.REG_DETECTION_OPTIMIZE, 0xC3)
            self.writeOnSPI(REG.REG_DETECTION_THRESHOLD, 0x0A)
        reply = self.readFromSPI(REG.REG_MODEM_CONFIG_2, 1)
        data = ((sf << 4) & 0xf0) + (reply[0] & 0x0F)
        self.writeOnSPI(REG.REG_MODEM_CONFIG_2, data)

    #This function will get the Spreading factor from module
    def getSpreadingFactor(self, sf):
        ans = self.readFromSPI(REG.REG_MODEM_CONFIG_2, 1) >> 4
        return ans
    
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
    def setSignalBandwidth(self, bandWidth):
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
        reply = self.readFromSPI(REG.REG_MODEM_CONFIG_1, 1)
        data = (reply[0] & 0x0F) | (bw << 4) 
        self.writeOnSPI(REG.REG_MODEM_CONFIG_1, data)
    
    #This function will get the BandWidth of the chip
    def getSignalBandwidth(self):
        ans = self.readFromSPI(REG.REG_MODEM_CONFIG_1) >> 4
        bw = "Error"
        if ans == 0:
            bw = "7.8 KHz"
        elif ans == 1:
            bw = "10.4 KHz"
        elif ans == 2:
            bw = "15.6 KHz"
        elif ans == 3:
            bw = "20.8 KHz"
        elif ans == 4:
            bw = "31.25 KHz"
        elif ans == 5:
            bw = "41.7 KHz"
        elif ans == 6:
            bw = "62.5 KHz"
        elif ans == 7:
            bw = "125 KHz"
        elif ans == 8:
            bw = "250 KHz"
        elif ans == 9:
            bw = "500 KHz"
        return bw

    #This function will enable or disable crc check.
    def setCrcCheck(self, crcCheck):
        if self.CRC:
            reply = self.readFromSPI(REG.REG_MODEM_CONFIG_2, 1)
            data = reply[0] | 0x04
            self.writeOnSPI(REG.REG_MODEM_CONFIG_2, data)
        else:
            reply = self.readFromSPI(REG.REG_MODEM_CONFIG_2, 1)
            data = reply[0] & 0xfb
            self.writeOnSPI(REG.REG_MODEM_CONFIG_2, data)

    # This function will set sync word
    def setSync(self, sw):
        self.writeOnSPI(REG.REG_SYNC_WORD, sw)

#   CRC ---------> Input Value
#   4/5 ---------> 1
#   4/6 ---------> 2
#   4/7 ---------> 3
#   4/8 ---------> 4

    #This function will change CRC on module
    def setCRC(self, cr):
        if cr < 5:
            cr = 5
        elif cr > 8 :
            cr = 8
        crc = 1
        if cr == 5:
            crc = 1
        elif cr == 6:
            crc = 2
        elif cr == 7:
            crc = 3
        elif cr == 8:
            crc = 4
        reply = self.readFromSPI(REG.REG_MODEM_CONFIG_1, 1)
        data = (reply[0] & 0xF0) | (crc << 1)
        self.writeOnSPI(REG.REG_MODEM_CONFIG_1, data);

    #This function will set carrier frequency
    def setFREQ(self, fr):
        freq = int(fr * 16384)
        msb = freq >> 16
        mid = (freq & 0xFFFF) >> 8
        lsb = (freq & 0xFF)
        self.writeOnSPI(REG.REG_FRF_MSB, msb)
        self.writeOnSPI(REG.REG_FRF_MID, mid)
        self.writeOnSPI(REG.REG_FRF_LSB, lsb)

    #This function will set the current protect registers
    def setOCP(self, mA):
        trim = 27
        if mA <= 120:
            trim = (mA - 45) / 5
        elif mA <= 240:
            trim = (mA + 30) / 10
        self.writeOnSPI(REG.REG_OCP, 0x20 | (0x1F & int(trim)))

    #This function will set output power (PA_Conf is 1)
    def setPWR(self, pwr, RFO):
        if RFO == True:
            if pwr < 0:
                pwr = 0
            elif pwr > 14:
                pwr = 14
            self.writeOnSPI(REG.REG_PA_CONFIG, pwr | 0x70)
        else:
            if pwr > 17:
                if pwr > 20:
                    pwr = 20
                pwr = pwr - 3
                self.writeOnSPI(REG.REG_PA_DAC, 0x87)
                self.setOCP(140)
            else:
                if pwr < 2:
                    pwr = 2
                self.writeOnSPI(REG.REG_PA_DAC, 0x84)
                self.setOCP(100)
            self.writeOnSPI(REG.REG_PA_CONFIG, (pwr-2) | PACONFIG.PA_BOOST)

    #This function will config the module
    def powerUP(self):
        self.reset()
        self.changeWorkingMode("Sleep")
        payload = self.readFromSPI(0x01, 1)
        self.writeOnSPI(0x01, payload[0] | 0x80)
        self.setFREQ(self.frequency)
        self.setPWR(self.power, self.RFO)
        self.writeOnSPI(0x0C, 0x23)                           #This line active maximum gain sensivity
        payload = self.readFromSPI(0x1E, 1)
        #self.writeOnSPI(0x1E, payload[0] | 0x03)              #This line will disable CRC
        self.writeOnSPI(0x1F, 0xFF)                           #Set receiver timeout to maximum (On single Mode)
        self.setSpreadingFactor(self.spreadingFactor)
        self.setCrcCheck(self.CRC)
        self.setSignalBandwidth(self.bandWidth)
        self.setCRC(self.crcRate)
        self.setSync(self.syncWord)
        self.writeOnSPI(0x20, self.preamble >> 8)
        self.writeOnSPI(0x21, self.preamble & 0xFF)
        payload = self.readFromSPI(0x40, 1)
        self.writeOnSPI(0x40, payload[0] | 0x3F)               # Map DIO0 To Receive
        self.changeWorkingMode("Standby")
        self.changeWorkingMode("ReceiveCON")
        if self.checkConnection():
            reply = self.readFromSPI(0x39, 1)
            return True
        else:
            return False

    #This function will send payload on LoRa
    def transmit(self, msg, timeout):
        length = len(msg)
        self.changeWorkingMode("Standby")
        payload = self.readFromSPI(REG.REG_FIFO_TX_BASE_ADDR, 1)
        self.writeOnSPI(REG.REG_FIFO_ADDR_PTR, payload[0])
        self.writeOnSPI(REG.REG_PAYLOAD_LENGTH, length)
        self.burstWrite(REG.REG_FIFO, msg)
        self.changeWorkingMode("Transmit")
        state = True
        while True:
            payload = self.readFromSPI(0x12, 1)
            if((payload[0] & 0x08) != 0):
                self.writeOnSPI(REG.REG_IRQ_FLAGS, IRQMASKS.IRQ_TX_DONE_MASK)
                self.workingMode("ReceiveCON")
                state = True
                break
            else:
                timeout = timeout - 1
                if timeout == 0:
                    self.changeWorkingMode("ReceiveCON")
                    state = False
                    break
                time.sleep(0.001)
        return state

    #This function will read payload from LoRa
    def read(self):
        self.changeWorkingMode("Standby")
        payload = self.readFromSPI(REG.REG_IRQ_FLAGS, 1)
        message = []
        if self.CRC:
            if payload[0] & 0x50 == 0x50:
                self.writeOnSPI(REG.REG_IRQ_FLAGS, IRQMASKS.IRQ_RX_DONE_MASK)
                bytesLen = self.readFromSPI(REG.REG_RX_NB_BYTES, 1)
                payload = self.readFromSPI(REG.REG_FIFO_RX_CURRENT_ADDR, 1)
                self.writeOnSPI(REG.REG_FIFO_ADDR_PTR, payload[0])
                message = self.readFromSPI(REG.REG_FIFO, bytesLen[0])
            else:
                print("false CRC")
        else:
            self.writeOnSPI(REG.REG_IRQ_FLAGS, IRQMASKS.IRQ_RX_DONE_MASK)
            bytesLen = self.readFromSPI(REG.REG_RX_NB_BYTES, 1)
            payload = self.readFromSPI(REG.REG_FIFO_RX_CURRENT_ADDR, 1)
            self.writeOnSPI(REG.REG_FIFO_ADDR_PTR, payload[0])
            message = self.readFromSPI(REG.REG_FIFO, bytesLen[0])
        self.writeOnSPI(REG.REG_IRQ_FLAGS, IRQMASKS.IRQ_RX_DONE_MASK)
        self.changeWorkingMode("ReceiveCON")
        return message
        
