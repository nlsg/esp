#!/usr/bin/env python

import webrepl

def do_connect(ssid, pwd):
    """a safe way to connect to a network"""
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect('lbbfairphone', 'ini_spot_smona')

webrepl.start(password="")
