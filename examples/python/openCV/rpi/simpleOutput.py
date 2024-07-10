#!/usr/bin/python3
# https://gpiozero.readthedocs.io/en/stable/recipes.html#led

from gpiozero import LED
from time import sleep

red = LED(17)

while True:
    red.on()
    sleep(1)
    red.off()
    sleep(1)
