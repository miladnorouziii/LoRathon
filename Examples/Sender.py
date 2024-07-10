from LoRa import LoRa
import time

# define LoRa module pins and configs.
resetPin = 25
DIO0Pin = 27
Frequency = 434
SF = 7
BW = 125
crc = 5
power = 17
RFO = False
crcCheck = True
syncWord = 56 #In decimal format eq to 0x38
lora = LoRa(resetPin, Frequency, SF, BW, crc, power, RFO, crcCheck, syncWord)

message = "Hello, i'm from transmitter side."
messageBytes = bytes(message, 'utf-8')

if lora.powerUP():
    print("LoRa started successfully")
else:
    print("Failed to start LoRa. Exiting ...")

while True:
    print("Sending message on LoRa")
    if lora.transmit(list(messageBytes), 2000):
        print("Message sent successfully.\n")
    else:
        print("Failed to send message.\n")
    time.sleep(7)