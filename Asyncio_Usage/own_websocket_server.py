#!/usr/bin/env python3

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send("Prefix" + message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
