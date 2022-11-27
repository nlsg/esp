#!/usr/bin/env python3

# from microdot_asyncio import Microdot

# app = Microdot()

# @app.route('/')
# async def hello(request):
#     print(f"served 'hello' \n{request=}")
#     return 'Hello, world!'

# app.run()

from machine import Pin, Timer
t0 = Timer(0)
t0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:(print(t), (p := Pin(2,Pin.OUT)).value(not p.value())))
