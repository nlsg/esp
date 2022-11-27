#!/usr/bin/env python3

"""this module is currently not working!!!"""
import uasyncio
async def repl(**options):
    """this is a simple repl, which is started as a coroutine,
    means that this runs asynchronously and makes the use of
    async/await usable"""
    get_in = lambda i: input("\n" + i + "\n!>>")
    msg = "Started urepl successfully"
    while True:
        inp = await get_in(msg)[:-1]
        print("!   got input")
        if isinstance(inp, str):
            msg = eval(inp)
        else: msg = "\n"
        print(f"!   evaled: {msg}")
