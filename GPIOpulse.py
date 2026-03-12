# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 13:20:00 2025

@author: kawdi
"""

import usb
import usb.util
import adafruit_blinka
import os
import board
import digitalio

os.environ['BLINKA_FT232H'] = "1"

def gpio_pulse(state):
    led = digitalio.DigitalInOut(board.C0)
    led.direction = digitalio.Direction.OUTPUT
    led.value = state