# API for LoRathon lib
First, you need to install the library using pip. See the Readme file for installation.
# Include Library
To include the library in your code simply add the below line in the first line of your code.
> from LoRa import LoRa

# Configuration
> lora = LoRa(Rst pin, Frequency, SpreadingFactor, BandWidth, CodingRate, Power, RFO, CRCCheck, SyncWord)

Pass your desired configuration. Check the below table for more information about arguments:

| Argument | Description|
| -----------| -------|
|Rst pin | Hardware reset the module|
|Frequency | carrier frequency in MHz [433-868-915] |
|Spreading Factor | Change the spreading factor of the radio, Choose between 6 to 12|
|Band Width | Change the signal bandwidth of the radio (in KHz). [7.8 - 10.4 - 15.6 - 20.8 - 31.25 - 41.7 - 62.5 - 125 - 250 - 500]|
|Coding Rate | Change the coding rate of the radio. Choose between 5 to 8.|
|Power | Change the TX power of the radio. Choose between 2 to 20.|
|RFO | PA Boost or RFO. if you have PA Boost, set RFO to False|
|CRC Check | Enable or disable CRC. True for enabling CRC and False to disable it.|
|Sync Word | Change the sync word of the radio, and Pass it in Decimal format.|

check the example folder to see the configuration.

# Functions
* ## lora.setFREQ(frequency):
      pass the frequency in MHz. Choose between 433MHz, 868MHz, 915MHz.
  
* ## lora.changeWorkingMode(Mode):
      Change the working mode manually. choose between "Sleep", "Standby", "Transmit", "ReceiveCON", "ReceiveSIN".
      Note that this version of the library doesn't support single receive.

* ## lora.checkConnection():
      Check LoRa connection, returns True if LoRa is connected, and returns False if LoRa isn't connected.

* ## lora.reset()
      This function will reset the LoRa module.

* ## lora.setSpreadingFactor(sf):
      Change spreading factor of radio. Pass the value between 6 to 12.

* ## lora.getSpreadingFactor():
      Returns spreading factor of radio

* ## lora.setSignalBandwidth(bw):
      Change the signal bandwidth of the radio (in KHz). Pass the value between these values.[7.8 - 10.4 - 15.6 - 20.8 - 31.25 - 41.7 - 62.5 - 
      125 - 250 - 500]

* ## lora.getSignalBandwidth():
      Returns Signal BandWidth of radio.

* ## lora.setCrcCheck(crc)
      Enable or Disable CRC Check. Pass True to enable CRC or False to disable crc

* ## lora.setSync(sw):
      Change the sync word of the radio. Pass it in decimal format.

* ## lora.setCRC(cr):
      Change the coding rate of the radio. Choose between 5 to 8. For example 5 for 4/5,

* ## lora.setOCP(mA):
      Over Current Protection. Pass in milliamp format, for example, 120.

* ## lora.setPWR(pwr, RFO):
      Change the TX power of the radio. Pass power and RFO. If you have a PA Boost module, set RFO to False.

* ## lora.powerUP():
      Start the radio with the given configures.

* ## lora.transmit(msg, timeout)
      Transmit messages on the Air. See the example folder.

* ## lora.read():
      Read the module payload after receiving the message. See the example folder.
