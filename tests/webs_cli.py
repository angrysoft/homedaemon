#!/usr/bin/python3
import asyncio
import websockets

async def hello(uri):
    while True:
        async with websockets.connect(uri) as websocket:
            # await websocket.send("Hello world!")
            data = await websocket.recv()
            print(data)

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:9000'))
