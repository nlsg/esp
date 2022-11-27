#!/usr/bin/env python3

import uasyncio
from microdot_asyncio import Microdot, Response
from urequests import get as get_request
from micro_func import Debug, has, trying, tee, callif
from time import time, localtime
from machine import RTC
import gpio

gpio_functions = {"status": gpio.status,
                    "get": gpio.get_pin,
                    "set": gpio.set_pin,
                    "read": gpio.read_pin,
                    "pwm": gpio.pwm_pin,
                    "ds18": gpio.read_ds18b20}

callback = lambda p: get_request(f"http://192.168.43.66:5000/{p}")
db = Debug("api")

get_documentation = lambda f: {
    "name": f.__name__,
    "route": trying(AttributeError,lambda x: x.__route__, f, lambda _, _i, a:"not routed!"),
    "docstr": f.__doc__
}

respond = lambda *a: Response(tee(callback, *a))
respond = lambda *a: Response(*a, headers={"Access-Control-Allow-Origin": "*"})

app = Microdot()

stat = {"callCount": 0,
        "startup": RTC().datetime()}

print("time! ", time())
print("localtime! ", localtime())

@app.before_request
def before_request_handler(request):
  global stat
  stat["callCount"] += 1
  db(f"payload: {request.args}")


############################################################################
#  ____                                        _        _   _              #
# |  _ \  ___   ___ _   _ _ __ ___   ___ _ __ | |_ __ _| |_(_) ___  _ __   #
# | | | |/ _ \ / __| | | | '_ ` _ \ / _ \ '_ \| __/ _` | __| |/ _ \| '_ \  #
# | |_| | (_) | (__| |_| | | | | | |  __/ | | | || (_| | |_| | (_) | | | | #
# |____/ \___/ \___|\__,_|_| |_| |_|\___|_| |_|\__\__,_|\__|_|\___/|_| |_| #
############################################################################

@app.route("/")
async def root(request):
  """the root node"""
  return respond({"doc": "/api/doc"})


##############################################
#  _                  _                   _  #
# | |    _____      _| |    _____   _____| | #
# | |   / _ \ \ /\ / / |   / _ \ \ / / _ \ | #
# | |__| (_) \ V  V /| |__|  __/\ V /  __/ | #
# |_____\___/ \_/\_/ |_____\___| \_/ \___|_| #
##############################################

@app.route("/api/util/ms/<int:time>")
async def api_documentation(request, time):
  await uasyncio.sleep_ms(time)
  request.args.update({"util/ms/": time})
  return respond(request.args)


@app.route("/api/gpio/<function>/<int:pin>")
@app.route("/api/gpio/<function>/<int:pin>/")
async def api_gpio(request, function, pin):
    """api rout"""

    response = gpio_functions[function](pin, **request.args)
    if has(response, "error"):
        pass
    return respond(dict(pin=pin,
                        value=response,
                        function=gpio_functions[function].__name__,
                        payload=request.args))


@app.route("/api/batch/<function>/<pins>")
@app.route("/api/batch/<function>/<pins>/")
def api_batch(request, function, pins):
  try:
    pins = (int(p) for p in pins.split("+"))
  except (TypeError, ValueError) as e:
    return respond({"error":e})
  return respond(dict(values={pin:gpio_functions[function](pin) for pin in pins},
                      function=gpio_functions[function].__name__,
                      payload=request.args))


#############################################
#  ____  _        _   _     _   _           #
# / ___|| |_ __ _| |_(_)___| |_(_) ___ ___  #
# \___ \| __/ _` | __| / __| __| |/ __/ __| #
#  ___) | || (_| | |_| \__ \ |_| | (__\__ \ #
# |____/ \__\__,_|\__|_|___/\__|_|\___|___/ #
#############################################

@app.route("/api/stat/api")
@app.route("/api/stat/api/")
def api_os(request):
  return respond(stat)

@app.route("/api/stat/esp/<tags>")
@app.route("/api/stat/esp/<tags>/")
def api_os(request, tags):
    tags = tags.split("+")
    stat = dict()
    if "all" in tags:
      tags = ("os", "sys", "machine", "esp", "esp32", "network", "micropython")
    if "os" in tags:
      from os import uname, listdir
      stat.update({"os":{"uname":str(uname()),
                         "listdir":listdir()}})
    if "sys" in tags:
      import sys
      stat.update({"sys":{"implementation": str(sys.implementation),
                          "version":  str(sys.version),
                          "platform": str(sys.platform),
                          "modules":  tuple(k for k in sys.modules),
                          "path":     sys.path,
                          "argv":     sys.argv}})
    if "machine" in tags:
      from machine import freq, unique_id
      stat.update({"machine":{"freq":       freq(),
                              "unique_id":  unique_id()}})
    if "esp" in tags:
      from esp import flash_size
      stat.update({"esp":{"flash_size":flash_size()}})
    if "esp32" in tags:
      from esp32 import raw_temperature, hall_sensor
      stat.update({"esp32":{"raw_temperature":  raw_temperature(),
                            "hall_sensor":      hall_sensor()}})
    if "network" in tags:
      stat.update({"network":"N/A"})
    if "micropython" in tags:
      from micropython import opt_level, mem_info, qstr_info, stack_use
      stat.update({"micropython":{"opt_leve":  opt_level(),
                                  "mem_info":  str(mem_info()),
                                  "qstr_info": str(qstr_info()),
                                  "stack_use": stack_use()}})

    return respond(stat)



Debug("microdot")("starting server")

# app.run(debug=True)



from machine import Pin

async def dummy_coro(pin):
    while True:
        pin.value(not pin.value())
        await uasyncio.sleep_ms(500)


coro = app.start_server(debug=True)
run_coro = lambda: uasyncio.run(coro)

async def main():
    uasyncio.create_task(app.start_server(debug=True))
    uasyncio.create_task(dummy_coro(Pin(2, Pin.OUT)))
    while True:
        await uasyncio.sleep_ms(2_000)

# uasyncio.run(main())
