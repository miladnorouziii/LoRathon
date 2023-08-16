import RPi.GPIO as GPIO
import time
import LoRathon as LoRa

DIO_PIN1 = 17
GPIO.setmode(GPIO.BCM)
msgCount = 0

lora = LoRa(434, 7, 125, 5, 17, False, True, 56)

def loraMsgReceived(channel):
    try:
        mens=bytes(lora.read()).decode("ascii",'ignore')
        print ("\n== LORA RECEIVE: ", mens)
    except Exception as e:
        print(e)

GPIO.setup(DIO_PIN1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(DIO_PIN1, GPIO.RISING,callback = loraMsgReceived)

if lora.powerUP():
    print("LoRa started successfully")
else:
    print("Failed to start LoRa. Exiting ...")

while True:
    time.sleep(5)
    print("You received ", msgCount, "messages")

