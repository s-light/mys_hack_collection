#!/usr/bin/python3

from gpiozero import LED
from time import sleep

LED1 = LED(4)

while True:
    LED1.on()
    sleep(1)
    LED1.off()
    sleep(1)