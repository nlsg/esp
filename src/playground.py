#!/usr/bin/env python3

import machine as m
import time as t
import gpio
import onewire, ds18x20
from micro_func imprt DB

db = DB("playground")

db("loaded playground")

def gpio_read():
    while True:
        db(gpio.read_pin(36))
        t.sleep(.25)

def ds18b20(pin, delay=5):
    """https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/"""
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(m.Pin(pin)))
    roms = ds_sensor.scan()
    db('Found DS devices: ', roms)
    while True:
        ds_sensor.convert_temp()
        t.sleep(.75)
        for rom in roms:
            db(rom)
            db(ds_sensor.read_temp(rom))
        t.sleep(delay)

def read_pin(pin):
    adc = m.ADC(m.Pin(pin, m.Pin.IN))
    adc.atten(m.ADC.ATTN_11DB)
    while True:
        t.sleep(.2)
        val_u16 = adc.read_u16()
        percentage = (val_u16 / 65535) * 100
        db(f"Reading ADC:\n{adc.read()=}\n{val_u16=}\n{percentage=}%")
