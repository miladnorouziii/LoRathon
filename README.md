# LoRa Library based on Python
This library is for LoRa modules (Sx127x) based on the Python language and has been tested on:
* Raspberry Pi Zero W
* Raspberry Pi 3B
* and Raspberry Pi 4.
# Ra01/02 pins:
<img src="https://github.com/Miladnorouzi77/LoRathon/assets/32528196/0bc675ac-c290-40a2-b215-b1e692aad894" width="300" height="300">

# Connection to Raspberry Pi:
You can change DIO0 to DIO5, RESET, and NSS pins and assign them your desired pins.
| SX127x Pin | Raspberry Pi Pin|
| -----------| -------|
|SCLK Pin| GPIO 11|
|MISO Pin| GPIO 9|
|MOSI Pin| GPIO 10|
|NSS Pin| GPIO 8|
|RST Pin| Desire|
|DIO0 Pin| Desire|
|DIO1 Pin| Desire|
|DIO2 Pin| Desire|
|DIO3 Pin| Desire|
|DIO4 Pin| Desire|
|DIO5 Pin| Desire|

# NOTES:
* Some boards (like the Raspberry Pi Zero W), cannot supply enough current for TX mode. So, use an external 3.3V supply that can provide at least 120mA. (Or use lower Transmitting power)
* These modules work with 3.3v (Or a maximum voltage equal to 3.7v), so be careful and don't connect your module to 5v, otherwise, you will damage your module.

# Installation:
To install the package use the below command:
> sudo pip3 install LoRathon

Requirement packages will be installed automatically.

# API:
Check [API.md](API.md) file for usage toturial.

# Toturial
https://medium.com/@miladnorouzi77/lora-with-raspberry-pi-c5bda3103d8d
