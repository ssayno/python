#!/usr/bin/env python3
import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8765/") as websocket_client_:
        print('ok')
        while True:
            req_msg = input("Please input your message: ")
            if not req_msg:
                continue
            if req_msg == 'exit':
                break
            await websocket_client_.send(req_msg)
            resp_msg = await websocket_client_.recv()
            print('[Server]:', resp_msg)

asyncio.run(hello())
