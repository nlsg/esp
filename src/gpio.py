#!/usr/bin/env python3

from machine import Pin, Timer, ADC, PWM
from time import sleep
from pt100 import PT100
import onewire, ds18x20  # ds1820b
from micro_func import trying, has, Debug, remove_chars

IO_MAPS = dict(
  input_only=(34, 35, 36, 39),
  pull_up=(14, 16, 17, 18, 19, 21, 22, 23),
  no_pull_up=(13, 25, 26, 27, 32, 33),
  dac=(25, 26),
  adc=(37,38,39,32,33,34,35,4,0,2,15,13,12,14,27,25,26),
  not_adc=(23, 22, 1, 3, 21, 19, 18, 5, 17, 16),
  touch=(4, 2, 15, 32, 33, 27, 14, 12, 13),
  high_speed=(14, 12, 13, 23, 18, 5, 17, 16, 4, 2, 15),
  tx=1,
  rx=3,
  scl=22,
  sda=26,
  spi_D=8,
  spi_WP=10,
  spi_HD=9,
  spi_Q=7,
  spi_CLK=6,
  spi_CS0=11,
)


def status(pin):
  pin = Pin(pin)
  print(pin)
  return dict(# mode=trying(AttributeError, pin.mode, lambda _, _i, _j: "N/A"),
              pull=trying(AttributeError, pin.pull, lambda _, _i, _j: "N/A"),
              drive=trying(AttributeError, pin.drive, lambda _, _i, _j: "N/A"))

# inputs
def get_pin(pin=None, **kwargs):
  """get the value of a digital output pin
  arguments:
  - pin: the pin on which a value is read
  return -> value of the pin"""
  return Pin(pin)()

def read_pin(pin):
  """read the value of a pin,
  which needs to have an internal ADC
  arguments:
    - pin:  the pin in which the value will be read
    - unit: the unit in which the read value should be interpreted,
            possible units are:
            - raw [12bit value] <default>
            - voltage [volt]
            - resistance [ohm]
            - pt100 [floating point in degres celsius]"""
  def read_pt100(pin, sample_size=10, delay=.1, **kwargs):
    pt100 = PT100(pin)
    values = []
    for _ in range(sample_size):
      values.append(pt100.read())
      sleep(delay)
    return sum(values) / sample_size

  adc = ADC(Pin(pin, Pin.IN))
  adc.atten(ADC.ATTN_11DB)
  read = adc.read()
  return {"raw_u16": adc.read_u16(),
          "raw": adc.read(),
          "%": (read  / 4096) * 100,
          "U": read * 3.3 / 4096,
          "t": read_pt100(pin),
          "R": 3.}

def read_ds18b20(pin):
  """reads temperature from a ds18b20 or ds18b20 sensors
  to support multiple sensors on one pin,
  the values are returned in a dict {"addr": val}
    - addr: 64bit hex address-string
    - val:  value in degres represented as float

  the data pin of the ds18b20 sensor
  must be pulled up by a 4.7 kOhm resistor"""

  ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(pin)))
  # roms = ds_sensor.scan()
  ds_sensor.convert_temp()
  # sleep(.75)

  # the standard string representation
  # of bytearrays is not sutable for dict-keys
  rm_list = ("bytearray", "(", ")", "b'", "\\", "x")
  fmt = lambda s: "x" + remove_chars(str(s), rm_list)

  return {fmt(rom): ds_sensor.read_temp(rom) for rom in ds_sensor.scan()}

# outputs
def set_pin(pin, value=None, **kwargs):
  """set the pin to value
  arguments:
    - pin:    to pin to act on
    - value:  to set the pin to (0,1)
              default value is None, in this case,
              the pin will toggle
  return -> value of the pin ( probably status feedback )"""

  pin = Pin(pin, Pin.OUT)
  if value is None:
    value = not pin()
  else:
    value = trying(ValueError, int, value,
                    lambda _, _i, a: {"error": f"ValueError: '{a}' is of wrong type!"})
    if has(value, "error"):
      return value
  pin(value)
  return pin()

def pwm_pin(pin, freq=None, duty=None):
  """set pwm value of given pin
  arguments:
    - pin:    the pin on which a pwm value will be set
    - freq
  https://docs.micropython.org/en/latest/library/machine.PWM.html#machine-pwm
  """
  args = {"pin":pin}
  if freq is not None:
    freq = trying(ValueError, int, lambda e, f, a: {"error":"{a} must be an integer"})
    if has(freq, "error"):
      return freq
    if 1000 < freq < 40_000:
      args["freq"] = freq
  if duty is not None:
    duty = trying(ValueError, int, lambda e, f, a: {"error":"{a} must be an integer"})
    if has(duty, "error"):
      return duty
    if 0 <= duty < 1024:
      args["duty"] = duty
  if len(args) < 2:
    return {"error":"ParameterError, you must supply eater 'freq' or 'duty' parameter"}
  pin = PWM(Pin(pin, Pin.OUT))
  return {"type": "PWM"}

