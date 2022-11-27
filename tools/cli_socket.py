import websockets
#!/usr/bin/env python

import asyncio
import websockets

uri = "ws://192.168.43.31:8266"

async def hello():
    msg = ""
    async with websockets.connect(uri) as websocket:
        await websocket.send(msg)
        msg = input(">>>" + await websocket.recv())

asyncio.run(hello())
