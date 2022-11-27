#!/usr/bin/env python3

from time import sleep
from machine import Pin, ADC
from pt100 import PT100


pt1= PT100(33)
while True:
    sample_size = 10
    delay = .2
    values = []
    for i in range(sample_size):
        values.append(pt1.read())
        sleep(delay)
    temp1 = sum(values) / sample_size

    temp1_ = pt1.read()
    ref_voltage = 3.3
    # voltage = raw_value * ref_voltage / 4096
    print(f"{temp1=} - {temp1_=} - {values=}")
    sleep(.5)
