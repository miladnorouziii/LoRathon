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

