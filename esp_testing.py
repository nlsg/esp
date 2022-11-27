from machine import Pin, PWM, ADC

pwm0 = PWM(Pin(23), freq=25000)  # create and configure in one go
pwm0 = PWM(Pin(23))         # create PWM object from a pin
pwm0.freq()         # get current frequency (default 5kHz)
pwm0.duty(0)             # set duty cycle from 0 to 1023 as a ratio duty/1023, (now 25%)
pwm0.duty()         # get current duty cycle, range 0-1023 (default 512, 50%)


adc0 = ADC(Pin(33))

def read_tacho():
  one_s = 1024
  tot = 0
  for i in range(one_s):
    tot += adc0.read()
  return tot/one_s

read_tacho()

duty_ns = pwm0.duty_ns()   # get current pulse width in ns
pwm0.duty_ns(250_000)      # set pulse width in nanoseconds from 0 to 1_000_000_000/freq, (now 25%)

pwm0.deinit()              # turn off PWM on the pin


import esp32
help(esp32)
help(esp32.NVS.get_blob)


import network
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points

wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('lbbfairphone', 'ini_spot_smona') # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
